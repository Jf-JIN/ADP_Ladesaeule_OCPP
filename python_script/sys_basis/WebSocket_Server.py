import asyncio
import websockets
from .XSignal import XSignal
from websockets.asyncio.server import ServerConnection  # 用于类型注释


class WebSocketServer:
    signal_recv = XSignal()

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__server = None
        self.__clients = set()
        self.__message_queue = asyncio.Queue()

    async def __aenter__(self):
        self.__server = await websockets.serve(self.__handle_client, self.host, self.port)
        self.__send_signal_recv('\n--<WebSocket_started> - <Server>')
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        在上下文管理器退出时关闭服务器
        """
        await self.__server.close()
        await self.__server.wait_closed()
        self.__send_signal_recv('--<WebSocket_closed>')

    async def __handle_client(self, websocket: ServerConnection):
        if websocket not in self.__clients:
            self.__clients.add(websocket)
        await websocket.send(f'<Responde> {websocket.remote_address}')
        await self.send(f'<Responde> {websocket.remote_address}')
        self.__send_signal_recv(f'--<Client_connected> {websocket.remote_address}')
        try:
            while True:
                message = await websocket.recv()
                self.__send_signal_recv(f'->>> received> {message}')
                self.signal_recv.emit(message)
                await self.__filter_for_ocpp(message=message)
        except websockets.ConnectionClosed as e:
            self.__send_signal_recv(f'--<Connection_closed> {e}')

    async def send(self, message):
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
        message = await self.__message_queue.get()
        return message

    async def __filter_for_ocpp(self, message: str):
        if message in [
            'Successfully connected to the server',
        ]:
            return
        if not (isinstance(message, str) and message.startswith('[')):  # 判断是否是Ocpp消息, 其特点为列表
            return
        await self.__message_queue.put(message)

    def __send_signal_recv(self, *args):
        """
        发送/打印 接收信号

        涵盖发送前的检查

        参数: 
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            self.signal_recv.emit(temp)
            print(temp)
        except Exception as e:
            error_text = f'********************\n<Error - send_signal_info> {e}\n********************'
            self.signal_recv.emit(error_text)
            print(error_text)


if __name__ == '__main__':
    async def start_server():
        server = WebSocketServer('localhost', 12345)  # 创建服务器
        server.signal_recv.connect(out)  # 信号 槽 连接
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
