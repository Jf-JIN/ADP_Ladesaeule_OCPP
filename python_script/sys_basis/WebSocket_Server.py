import asyncio
import websockets
from .XSignal import XSignal
from websockets.asyncio.server import ServerConnection  # 用于类型注释
from ocpp.messages import unpack, MessageType


class WebSocketServer:
    signal_recv = XSignal()

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__server = None
        self.__clients = set()
        self.__message_queue = asyncio.Queue()  # 创建消息队列

    async def __aenter__(self):
        self.__server = await websockets.serve(self.__handle_client, self.host, self.port)
        print('--<WebSocket_started>\n')
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        在上下文管理器退出时关闭服务器
        """
        # self.__ping_timer.cancel()
        await self.__server.close()
        await self.__server.wait_closed()
        print('--<WebSocket_closed>\n')

    async def __handle_client(self, websocket: ServerConnection):
        if websocket not in self.__clients:
            self.__clients.add(websocket)
        await websocket.send(f'<Responde> {websocket.remote_address}')
        await self.send(f'<Responde> {websocket.remote_address}')
        print(f'--<Client_connected> {websocket.remote_address}\n')
        try:
            while True:
                message = await websocket.recv()
                print(f'->recieved> {message}\n')
                self.signal_recv.emit(message)
                await self.__filter_for_ocpp(message=message)
        except websockets.ConnectionClosed as e:
            print(f'--<Connection_closed> {e}\n')

    async def send(self, message):
        for client in self.__clients.copy():
            client: ServerConnection
            try:
                await client.ping()
                print(f'<-send_to<{client.remote_address}\t{message}\n')
                asyncio.create_task(client.send(message))
            except websockets.ConnectionClosed:
                print(f'--<Client_disconnected> {client.remote_address}\n')
                self.__clients.remove(client)

    async def recv(self):
        message = await self.__message_queue.get()
        return message

    async def __filter_for_ocpp(self, message: str):
        # print('__filter_for_ocpp\t', repr(message))
        if message in [
            'Successfully connected to the server',
        ]:
            return
        if not (isinstance(message, str) and message.startswith('[')):  # 判断是否是Ocpp消息, 其特点为列表
            return
        await self.__message_queue.put(message)


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
