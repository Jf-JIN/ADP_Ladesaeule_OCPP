
import asyncio
import traceback
from threading import Thread
from script.sys_basis.XSignal import XSignal
from sys_basis.WebSocket_Client import WebSocketClient


class OCPPClientPort(Thread):
    def __init__(self, uri, charge_point_name, charge_point_version='v2.0.1', info_title='OCPP Client'):
        super().__init__()
        self.__signal_thread_client_info = XSignal()
        self.__signal_thread_client_recv_request = XSignal()
        self.__signal_thread_client_recv_response = XSignal()
        self.__websocket = WebSocketClient(uri)
        self.__list_request_message = []
        self.__list_response_message = []
        self.__event_request_message = asyncio.Event()
        self.__event_response_message = asyncio.Event()
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        if str(charge_point_version).lower() in ['v16', 'v1.6', 'v1_6', 'ocpp16', 'ocpp1.6', 'ocpp1_6']:
            from sys_basis.Charge_Point import ChargePointV16
            self.__charge_point = ChargePointV16(charge_point_name, self.__websocket)
        elif str(charge_point_version).lower() in ['v201', 'v2.0.1', 'v2_0_1', 'ocpp201', 'ocpp2.0.1', 'ocpp2_0_1']:
            from sys_basis.Charge_Point import ChargePointV201
            self.__charge_point = ChargePointV201(charge_point_name, self.__websocket)
        else:
            raise ValueError(
                f'Invalid charge point version: {charge_point_version}. Valid versions are: \n\t- "v16", "v1.6", "v1_6", "ocpp16", "ocpp1.6", "ocpp1_6", \n\t- "v2.0.1", "v2_0_1", "ocpp201", "ocpp2.0.1", "ocpp2_0_1".')
        self.__charge_point.signal_charge_point_ocpp_request.connect(self.signal_thread_client_recv_request.emit)
        self.__charge_point.signal_charge_point_ocpp_response.connect(self.signal_thread_client_recv_response.emit)
        self.__charge_point.signal_charge_point_info.connect(self.signal_thread_client_info.emit)

    @property
    def signal_thread_client_info(self):
        return self.__signal_thread_client_info

    @property
    def signal_thread_client_recv_request(self):
        return self.__signal_thread_client_recv_request

    @property
    def signal_thread_client_recv_response(self):
        return self.__signal_thread_client_recv_response

    def send_request_message(self, message):
        """ 
        发送请求信息
        """
        self.__list_request_message.append(message)
        self.__event_request_message.set()

    def send_response_message(self, message):  # TODO 缺少成功与否的返回值
        """ 
        发送响应信息
        """
        self.__list_response_message.append(message)
        self.__event_response_message.set()

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        self.__send_signal(signal=self.signal_thread_client_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

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

    async def __listen_for_messages(self):
        while True:
            message = await self.__websocket.recv()
            if (isinstance(message, str) and message.startswith('[')):  # 信息过滤
                await self.__charge_point.route_message(message)

    async def __send_request_messages(self):
        while True:
            await self.__event_request_message.wait()
            try:
                # 此处结果将由 __charge_point.signal_charge_point_ocpp_response 传递, 无需手动处理
                await self.__charge_point.send_request_message(self.__list_request_message.pop(0))
            except:
                self.__send_signal_info(f'<Error - send_request_message>\n{traceback.format_exc}')
            if self.__list_request_message:
                self.__event_request_message.clear()

    async def __send_response_messages(self):
        while True:
            await self.__event_response_message.wait()
            try:
                result = await self.__charge_point.send_response_message(self.__list_response_message.pop(0))  # result 为 True 或 False, 分别表示成功或失败
            except:
                self.__send_signal_info(f'<Error - send_request_message>\n{traceback.format_exc}')
            if self.__list_response_message:
                self.__event_response_message.clear()

    async def __start_charge_point_loop(self):
        async with self.__websocket:
            self.__task_listening = asyncio.create_task(self.__listen_for_messages())
            setattr(self.__task_listening, 'task_name', 'task_listening')
            self.__task_send_request_messages = asyncio.create_task(self.__send_request_messages())
            setattr(self.__task_listening, 'task_name', 'task_send_request_messages')
            self.__task_send_response_messages = asyncio.create_task(self.__send_response_messages())
            setattr(self.__task_listening, 'task_name', 'task_send_response_messages')
            await asyncio.gather(self.__task_listening, self.__task_send_request_messages, self.__task_send_response_messages)
            await asyncio.Future()

    def stop(self):
        """取消监听任务"""
        for task in [self.__task_listening, self.__task_send_request_messages, self.__task_send_response_messages]:
            if task:
                task.cancel()
                self.__send_signal_info(f'<Task Cancel> {task.task_name} is canceled')

    def run(self):
        asyncio.run(self.__start_charge_point_loop())
