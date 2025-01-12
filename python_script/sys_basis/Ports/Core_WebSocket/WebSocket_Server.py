
import asyncio
import traceback
import websockets
from sys_basis.XSignal import XSignal
from const.Const_Parameter import *
from websockets.asyncio.server import Server, ServerConnection  # 用于类型注释


class WebSocketServer(object):
    """
    WebSocket 服务端类
    - 使用上下文管理器

    - 参数:
        - host (str): WebSocket 服务器地址
        - port (int): WebSocket 服务器端口
        - info_title (str): WebSocket 服务器信息标题, 用于发送信号时显示信息来源, 默认为 `WebSocket Server`
        - ping_interval_s (int|float): 心跳间隔时间, 单位为秒, 须大于0, 默认值为 20
        - ping_timeout_s (int|float): 心跳超时时间, 单位为秒, 须大于0, 默认值为 20

    - 信号:
        - signal_websocket_server_recv: WebSocket 服务端接收信号
        - signal_websocket_server_info: 普通信号, 用于信息显示, 调试等

    - 属性:
        - server(Server): WebSocket 连接对象

    - 方法:
        - send(异步): 发送消息
        - recv(异步): 接收消息. 注意! 该函数是供OCPP使用, 不应被手动调用, 需要获取消息, 请通过信号 `signal_websocket_server_recv` 获取
    """

    def __init__(
        self,
        host: str,
        port: int,
        info_title: str | None = 'WebSocket_Server',
        recv_timeout_s: int | float = 30,
        ping_interval_s: int | float = 20,
        ping_timeout_s=20
    ) -> None:
        self.__signal_websocket_server_recv = XSignal()
        self.__signal_websocket_server_info = XSignal()
        self.__host = host
        self.__port = port
        self.__server = None
        self.__clients = set()
        self.__message_queue = asyncio.Queue()
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        if not isinstance(ping_interval_s, (int, float)) or ping_interval_s <= 0:
            self.__send_signal_info(
                f'<Error - __init__> ping_interval_s must be a positive integer or float. It has been set to 20. The provided type and value are {type(ping_interval_s)} | {ping_interval_s}')
            self.__ping_interval_s = 20
        else:
            self.__ping_interval_s = ping_interval_s
        if not isinstance(ping_timeout_s, (int, float)) or ping_timeout_s <= 0:
            self.__send_signal_info(
                f'<Error - __init__> ping_timeout_s must be a positive integer or float. It has been set to 20. The provided type and value are {type(ping_timeout_s)} | {ping_timeout_s}')
            self.__ping_timeout_s = 20
        else:
            self.__ping_timeout_s = ping_timeout_s
        self.__recv_timeout_s = recv_timeout_s if isinstance(recv_timeout_s, (int, float)) else 30

    @property
    def signal_websocket_server_recv(self) -> XSignal:
        """ WebSocket 服务端接收信号 """
        return self.__signal_websocket_server_recv

    @property
    def signal_websocket_server_info(self) -> XSignal:
        """ 普通信号, 用于信息显示, 调试等 """
        return self.__signal_websocket_server_info

    @property
    def server(self) -> None | Server:
        """ 服务器对象 """
        return self.__server

    async def send(self, message) -> None:
        """
        发送消息

        - 参数:
            - message: 消息内容, 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        for client in self.__clients.copy():
            client: ServerConnection
            try:
                await client.ping()
                self.__send_signal_info(f'<<<- Send_To - {client.remote_address}>  {message}')  # 使用 to 明确目标
                asyncio.create_task(client.send(message))
            except websockets.ConnectionClosed:
                self.__send_signal_info(f'--<Client_Disconnected> {client.remote_address}')
                self.__clients.remove(client)

    async def recv(self):
        """
        接收消息

        ### 注意! 该函数是供OCPP使用, 不应被手动调用, 需要获取消息, 请通过信号 `signal_websocket_server_recv` 获取
        """
        message = await self.__message_queue.get()
        return message

    async def __aenter__(self):
        """
        with 进入口
        """
        self.__server = await websockets.serve(self.__handle_client, self.__host, self.__port, ping_interval=self.__ping_interval_s, ping_timeout=self.__ping_timeout_s)
        self.__send_signal_info('--<WebSocket_Started> - <Server>')
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """
        关闭连接
        """
        if self.__server:
            await self.__server.close()
            await self.__server.wait_closed()
        self.__send_signal_info('--<WebSocket_Closed>')

    async def __handle_client(self, websocket: ServerConnection) -> None:
        """
        处理客户端连接

        在监听循环中, 每当有信息接收时将会通过 __filter_for_ocpp 方法向 OCPP 发送信息. 原理上是向队列中添加信息元素
        """
        if websocket not in self.__clients:
            self.__clients.add(websocket)
        await websocket.send(f'<Response> {websocket.remote_address}')
        await self.send(f'<Response> {websocket.remote_address}')
        self.__send_signal_info(f'--<Client_Connected> {websocket.remote_address}')
        try:
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=self.__recv_timeout_s)
                    self.__send_signal_info(f'->>> Received_From - {websocket.remote_address}>  {message}')  # 使用 from 明确来源
                    self.__send_signal_recv(message)
                    await self.__filter_for_ocpp(message=message)
                except asyncio.TimeoutError:
                    pass
                except Exception as e:
                    self.__send_signal_info(f'--<Exception> {traceback.format_exc()}')

        except websockets.ConnectionClosed as e:
            self.__send_signal_info(f'--<Connection_Closed> {traceback.format_exc()}')
        except Exception as e:
            self.__send_signal_info(f'--<Exception> {traceback.format_exc()}')

    async def __filter_for_ocpp(self, message: str) -> None:
        """
        过滤 Ocpp 消息, 其特征为列表形式的字符串, 以 '[' 开头

        - 参数:
            - message (str): 接收到的消息

        - 返回:
            - None 或 OCPP消息
        """
        if isinstance(message, str) and message.startswith('['):  # 判断是否是Ocpp消息, 其特点为列表
            await self.__message_queue.put(message)

    def __send_signal_recv(self, *args) -> None:
        """
        发送/打印 接收信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_websocket_server_recv, error_hint='send_signal_recv', log=Log.WS.info, doShowTitle=False, doPrintInfo=False, args=args)

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_websocket_server_info, error_hint='send_signal_info', log=Log.WS.info, doShowTitle=True, doPrintInfo=False, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=None) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        - 参数:
            - signal(XSignal): 信号对象
            - error_hint(str): 错误提示
            - log: 日志器动作
            - doShowTitle(bool): 是否显示标题
            - doPrintInfo(bool): 是否打印信息
            - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        if args is None:
            args = []
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
            error_text = f'********************\n<Error - {error_hint}> {traceback.format_exc()}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)
