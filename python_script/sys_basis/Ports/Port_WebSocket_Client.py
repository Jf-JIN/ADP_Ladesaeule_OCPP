

import asyncio
import json
import traceback
from sys_basis.XSignal import XSignal
from sys_basis.Ports.Core_WebSocket.WebSocket_Client import WebSocketClient


class WebSocketClientPort(object):
    def __init__(self, uri, info_title='Info_Client_Port'):
        super().__init__()
        self.__signal_thread_websocket_client_info = XSignal()
        self.__signal_thread_websocket_client_recv = XSignal()
        self.__websocket = WebSocketClient(uri, info_title='Info_WebSocket_Client')
        self.__websocket.signal_websocket_client_info.connect(self.signal_thread_websocket_client_info.emit)
        self.__websocket.signal_websocket_client_recv.connect(self.__handle_recv_message)
        self.__list_send_data = []  # 存储待发送消息, 当列表非空则持续发送, 当列表为空则相应事件(__event_request_message)等待
        self.__event_send_data = asyncio.Event()  # 发送消息事件
        self.__isRunning = True
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None

    @property
    def websocket(self) -> WebSocketClient:
        return self.__websocket

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    @property
    def signal_thread_websocket_client_info(self) -> XSignal:
        return self.__signal_thread_websocket_client_info

    @property
    def signal_thread_websocket_client_recv(self) -> XSignal:
        return self.__signal_thread_websocket_client_recv

    async def run(self) -> None:
        """
        异步协程主体
        """
        try:
            async with self.__websocket:
                self.__task_listening = asyncio.create_task(self.__listen_for_messages())
                self.__task_send_data = asyncio.create_task(self.__send_data())
                await asyncio.gather(
                    self.__task_listening,
                    self.__task_send_data
                )
                await asyncio.Future()
        except Exception as e:
            self.__send_signal_info(f"<Error - Websocket_Client_Port>\n{traceback.format_exc()}")
        finally:
            self.__isRunning = False

    def send_data(self, data):
        self.__list_send_data.append(data)
        self.__event_send_data.set()

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_thread_websocket_client_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
        - signal(XSignal): 信号对象
        - error_hint(str): 错误提示
        - log: 日志器动作
        - doShowTitle(bool): 是否显示标题
        - doPrintInfo(bool): 是否打印信息
        - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            if self.__info_title and doShowTitle:
                temp = f'< {self.__info_title} >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(temp)

    def __handle_recv_message(self, message: str) -> None:
        """
        处理接收到的消息

        消息内容将通过信号 signal_thread_websocket_client_recv 发送出去, 其类型可能为 str 或 dict

        参数: 
        - message: 接收到的消息
        """
        if message.startswith(f='{'):
            try:
                message = json.loads(message)
            except Exception as e:
                self.__send_signal_info(f'<Error> {e}')
        self.__send_signal_info(f'->>> Received> {message}')
        self.signal_thread_websocket_client_recv.emit(message)

    async def __listen_for_messages(self) -> None:
        """
        监听消息, 循环执行
        """
        while self.__isRunning:
            message = await self.__websocket.recv()
            self.__handle_recv_message(message)

    async def __send_data(self) -> None:
        """
        发送消息, 循环执行

        当 send_data 被调用时, 会将消息放入队列中, 然后通过此方法发送

        当信息列表 __list_send_data 为空时, 将等待事件 __event_send_data 触发
        """
        while self.__isRunning:
            await self.__event_send_data.wait()
            if not self.__isRunning:  # 提前终止
                break
            if self.__list_send_data:
                message = self.__list_send_data.pop(0)
                await self.__websocket.send(message)
                self.__send_signal_info(f'<<<- Sent> {message}')
            if len(self.__list_send_data) == 0:
                self.__event_send_data.clear()
