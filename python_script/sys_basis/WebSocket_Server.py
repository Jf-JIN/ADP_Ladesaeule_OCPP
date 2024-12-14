
import asyncio
import websockets
from .XSignal import XSignal
from websockets.asyncio.server import Server, ServerConnection  # 用于类型注释


class WebSocketServer(object):
    """ 
    WebSocket 服务端类
    - 使用上下文管理器

    参数: 
    - host (str): WebSocket 服务器地址
    - port (int): WebSocket 服务器端口
    - info_title (str): WebSocket 服务器信息标题, 用于发送信号时显示信息来源, 默认为 `WebSocket Server`

    信号: 
    - signal_websocket_server_recv: WebSocket 客户端接收信号
    - signal_websocket_server_info: 普通信号, 用于信息显示, 调试等

    属性: 
    - server(Server): WebSocket 连接对象

    方法: 
    - send(异步): 发送消息
    - recv(异步): 接收消息
    """

    def __init__(self, host: str, port: int, info_title: str | None = 'WebSocket Server') -> None:
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

    @property
    def signal_websocket_server_recv(self):
        return self.__signal_websocket_server_recv

    @property
    def signal_websocket_server_info(self):
        return self.__signal_websocket_server_info

    @property
    def server(self) -> None | Server:
        return self.__server

    async def send(self, message):
        """ 
        发送消息

        参数:
        - message: 消息内容, 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        for client in self.__clients.copy():
            client: ServerConnection
            try:
                await client.ping()
                self.__send_signal_recv(f'<<<- send_to< {client.remote_address}\t{message}')
                asyncio.create_task(client.send(message))
            except websockets.ConnectionClosed:
                self.__send_signal_recv(f'--<Client_disconnected> {client.remote_address}')
                self.__clients.remove(client)

    async def recv(self):
        """ 
        接收消息
        """
        message = await self.__message_queue.get()
        return message

    async def __aenter__(self):
        """
        with 进入口
        """
        self.__server = await websockets.serve(self.__handle_client, self.__host, self.__port)
        self.__send_signal_recv('\n--<WebSocket_started> - <Server>')
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """
        关闭连接
        """
        await self.__server.close()
        await self.__server.wait_closed()
        self.__send_signal_recv('--<WebSocket_closed>')

    async def __handle_client(self, websocket: ServerConnection) -> None:
        if websocket not in self.__clients:
            self.__clients.add(websocket)
        await websocket.send(f'<Responde> {websocket.remote_address}')
        await self.send(f'<Responde> {websocket.remote_address}')
        self.__send_signal_recv(f'--<Client_connected> {websocket.remote_address}')
        try:
            while True:
                message = await websocket.recv()
                self.__send_signal_recv(f'->>> received> {message}')
                self.signal_websocket_server_recv.emit(message)
                await self.__filter_for_ocpp(message=message)
        except websockets.ConnectionClosed as e:
            self.__send_signal_recv(f'--<Connection_closed> {e}')

    async def __filter_for_ocpp(self, message: str):
        """ 
        过滤 Ocpp 消息, 其特征为列表形式的字符串, 以 '[' 开头

        参数:
        - message (str): 接收到的消息

        返回: 
        - None 或 OCPP消息
        """
        if message in [
            'Successfully connected to the server',
        ]:
            return
        if not (isinstance(message, str) and message.startswith('[')):  # 判断是否是Ocpp消息, 其特点为列表
            return
        await self.__message_queue.put(message)

    def __send_signal_recv(self, *args) -> None:
        """
        发送/打印 接收信号

        涵盖发送前的检查

        参数: 
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        self.__send_signal(signal=self.signal_websocket_server_recv, error_hint='send_signal_recv', show_title=False, log=None, *args)

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        self.__send_signal(signal=self.signal_websocket_server_info, error_hint='send_signal_info', show_title=True, log=None, *args)

    def __send_signal(self, signal: XSignal, error_hint: str, show_title: bool = False, log=None, *args) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
        - signal(XSignal): 信号对象
        - error_hint(str): 错误提示
        - show_title(bool): 是否显示标题
        - log: 日志器动作
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            if self.__info_title and show_title:
                temp = f'< {self.__info_title} >\n' + temp
            signal.emit(temp)
            print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and show_title:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            print(error_text)
            if log:
                log(temp)


if __name__ == '__main__':
    async def start_server():
        server = WebSocketServer('localhost', 12345)  # 创建服务器
        server.signal_websocket_server_recv.connect(out)  # 信号 槽 连接
        async with server:  # 上下文管理器启动服务器
            # 这段注释的代码可以解注后运行, 用于测试
            # async def periodic_send():  # 一个测试, 每隔一秒发送一条消息
            #     while True:
            #         await server.send("Server Message")  # 调用方法, 向所有客户端发送消息
            #         await asyncio.sleep(1)  # 等待一秒
            # asyncio.create_task(periodic_send())
            await asyncio.Future()  # 保持运行

    def out(message):  # 槽函数
        print(f'out\t{message}\n')
    asyncio.run(start_server())  # 服务器 启动! 芜湖!
