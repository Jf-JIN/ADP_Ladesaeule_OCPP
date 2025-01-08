
import asyncio
import websockets
from sys_basis.XSignal import XSignal
from websockets.asyncio.client import ClientConnection  # 用于类型注释


class WebSocketClient(object):
    """
    WebSocket 客户端类
    - 使用上下文管理器

    - 参数:
        - uri (str): WebSocket 服务器地址
        - recv_timeout_s (int|float): 接收消息超时时间, 单位为秒, 须大于0, 默认值为 30.
        - retry_interval_s (int|float): 重试间隔时间, 单位为秒, 须大于0, 默认值为 1
        - max_retries (int): 最大重试次数, 默认值为-1, 表示无限重试
        - info_title (str): WebSocket 客户端信息标题, 用于发送信号时显示信息来源, 默认为 `WebSocket Client`
        - ping_interval_s (int|float): 心跳间隔时间, 单位为秒, 须大于0, 默认值为 20
        - ping_timeout_s (int|float): 心跳超时时间, 单位为秒, 须大于0, 默认值为 20

    - 信号:
        - signal_websocket_client_recv(str): WebSocket 客户端接收信号
        - signal_websocket_client_info(str): 普通信号, 用于信息显示, 调试等

    - 属性:
        - websocket(ClientConnection): WebSocket 连接对象

    - 方法:
        - connect(异步): 连接服务器
        - send(异步): 发送消息
        - recv(异步): 接收消息
    """

    def __init__(self, uri, recv_timeout_s: int | float = 30, retry_interval_s: int | float = 1, max_retries: int = -1, info_title: str | None = 'WebSocket_Client', ping_interval_s: int | float = 20, ping_timeout_s=20) -> None:
        self.__signal_websocket_client_recv = XSignal()  # WebSocket 客户端接收信号
        self.__signal_websocket_client_info = XSignal()  # 普通信号, 用于信息显示, 调试等
        self.__uri = uri
        self.__websocket = None
        if not isinstance(recv_timeout_s, (int, float)) or recv_timeout_s <= 0:
            self.__send_signal_info(
                f'<Error - __init__> recv_timeout_s must be a positive integer or float. It has been set to 30. The provided type and value are {type(recv_timeout_s)} | {recv_timeout_s}')
            self.__recv_timeout_s = 30
        else:
            self.__recv_timeout_s = recv_timeout_s
        if not isinstance(retry_interval_s, (int, float)) or retry_interval_s <= 0:
            self.__send_signal_info(
                f'<Error - __init__> retry_interval_s must be a positive integer or float. It has been set to 1. The provided type and value are {type(retry_interval_s)} | {retry_interval_s}')
            self.__retry_interval_s = 1
        else:
            self.__retry_interval_s = retry_interval_s
        if not isinstance(max_retries, int):
            self.__send_signal_info(f'<Error - __init__> max_retries must be an integer. It has been set to -1. The provided type is {type(max_retries)}')
            self.__max_retries = -1
        else:
            self.__max_retries = max_retries
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

    @property
    def websocket(self) -> ClientConnection:
        return self.__websocket

    @property
    def signal_websocket_client_recv(self) -> XSignal:
        return self.__signal_websocket_client_recv

    @property
    def signal_websocket_client_info(self) -> XSignal:
        return self.__signal_websocket_client_info

    async def connect(self) -> None:
        await self.__connect()

    async def send(self, message: str) -> None:
        """
        发送消息到服务器

        - 参数:
            - message (str): 要发送的消息, 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式
        """
        if self.__websocket is not None:
            try:
                self.__send_signal_info(f'<<<- Send< {message}')
                await self.__websocket.send(message)
            except (ConnectionAbortedError, websockets.exceptions.ConnectionClosedError) as e:
                self.__send_signal_info(f'--<Connection_Failed>: Connection closed, reconnecting... ({e})')
                self.__websocket = None
                await self.__connect()
                await self.send(message)

    async def recv(self):
        """
        接收服务器的消息
        """
        if self.__websocket is not None:
            try:
                response = await asyncio.wait_for(self.__websocket.recv(), timeout=self.__recv_timeout_s)
                self.__send_signal_recv(response)
                self.__send_signal_info(f'->>> Received> {response}')
                return response
            except asyncio.TimeoutError as e:
                await self.__websocket.ping()
            except websockets.exceptions.ConnectionClosedError as e:
                self.__send_signal_info(f'--<Connection_Failed>: Connection closed, reconnecting... ({e})')
                if self.__websocket is not None:
                    await self.__websocket.close()
                    self.__websocket = None
                await self.__connect()
                return await self.recv()

    async def __aenter__(self) -> ClientConnection:
        """
        with 进入口
        """
        await self.__connect()
        return self.__websocket

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """
        关闭连接
        """
        if self.__websocket is not None:
            await self.__websocket.close()
        self.__send_signal_info('--<WebSocket_Closed>')

    async def __connect(self):
        """
        连接服务器
        """
        self.__send_signal_info('--<Connecting>')
        retries = 0
        while retries < self.__max_retries or self.__max_retries < 0:
            try:
                self.__websocket = await websockets.connect(self.__uri, ping_interval=self.__ping_interval_s, ping_timeout=self.__ping_timeout_s)
                await self.__websocket.send('Successfully connected to the server')
                return self
            except (ConnectionRefusedError, websockets.exceptions.WebSocketException) as e:
                if self.__max_retries < 0:
                    self.__send_signal_info(f'--<Connection_Failed>: {e} Reconnecting...')
                elif retries <= self.__max_retries:
                    self.__send_signal_info(f'--<Connection_Failed>: {e} Reconnecting... ({retries}/{self.__max_retries})...')
                    retries += 1
                else:
                    self.__send_signal_info(f'--<Connection_Failed>: Unable to connect to the server. Maximum retry attempts reached. ({self.__max_retries})')
                await asyncio.sleep(self.__retry_interval_s)

    def __send_signal_recv(self, *args) -> None:
        """
        发送/打印 接收信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_websocket_client_recv, error_hint='send_signal_recv', log=None, doShowTitle=False, doPrintInfo=False, args=args)

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_websocket_client_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        - 参数:
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

# 使用示例


if __name__ == '__main__':
    async def websocket_client():
        uri = 'ws://localhost:12345'  # 服务器地址
        client = WebSocketClient(uri)  # 创建客户端
        async with client:  # 上下文管理器启动客户端

            # 这段注释的代码可以解注后运行, 用于测试
            # async def periodic_send():  # 一个测试, 每隔一秒发送一条消息
            #     while True:
            #         await client.send("Client message")  # 发送消息
            #         await asyncio.sleep(1)  # 等待一秒
            # asyncio.create_task(periodic_send())  # 启动发送消息的任务

            async def listen():  # 监听服务器返回的消息
                while client:
                    a = await client.recv()  # 接收消息
                    print(f'listen\t{a}\n')

            asyncio.create_task(listen())  # 启动监听任务
            await asyncio.Future()  # 保持运行

    # 启动客户端
    asyncio.run(websocket_client())
