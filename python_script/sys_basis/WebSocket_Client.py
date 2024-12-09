import asyncio
from decimal import Context
import websockets


class WebSocketClient(Context):
    def __init__(self, uri, recv_timeout_s=30, retry_interval_s=1, max_retries=-1):
        self.__uri = uri
        self.__websocket = None
        self.__max_retries = max_retries
        self.__retry_interval_s = retry_interval_s
        self.__recv_timeout_s = recv_timeout_s

    @property
    def websocket(self):
        return self.__websocket

    async def connection(self):
        await self.__connection()

    async def __aenter__(self):
        """
        with 进入口
        """
        await self.__connection()
        return self.__websocket

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        关闭连接
        """
        if self.__websocket is not None:
            await self.__websocket.close()

    async def __connection(self):
        """
        连接服务器
        """
        print('--<connecting>')
        retries = 0
        while retries < self.__max_retries or self.__max_retries < 0:
            try:
                self.__websocket = await websockets.connect(self.__uri, ping_interval=self.__recv_timeout_s, ping_timeout=1)
                await self.__websocket.send('Successfully connected to the server')
                return self
            except (ConnectionRefusedError, websockets.exceptions.WebSocketException) as e:
                if self.__max_retries < 0:
                    print(f'--<Connection_failed> : {e} Reconnecting...')
                elif retries <= self.__max_retries:
                    print(f'--<Connection_failed>: {e} Reconnecting... ({retries}/{self.__max_retries})...')
                    retries += 1
                else:
                    print(f'--<Connection_failed>: Unable to connect to the server. Maximum retry attempts reached. ({self.__max_retries})')
                await asyncio.sleep(self.__retry_interval_s)

    async def send(self, message):
        """
        发送消息到服务器
        """
        if self.__websocket is not None:
            try:
                print(f'<-send<: {message}')
                await self.__websocket.send(message)
            except (ConnectionAbortedError, websockets.exceptions.ConnectionClosedError) as e:
                print(f'--<Connection_failed>: Connection closed, reconnecting... ({e})')
                self.__websocket = None
                await self.__connection()
                await self.send(message)

    async def recv(self):
        """接收服务器的消息. """
        if self.__websocket is not None:
            try:
                response = await asyncio.wait_for(self.__websocket.recv(), timeout=self.__recv_timeout_s)
                print(f'>-recieved> {response}')
                return response
            except asyncio.TimeoutError as e:
                await self.__websocket.ping()
            except websockets.exceptions.ConnectionClosedError as e:
                print(f'--<Connection_failed>: Connection closed, reconnecting... ({e})')
                if self.__websocket is not None:
                    await self.__websocket.close()
                    self.__websocket = None
                await self.__connection()
                return await self.recieve()


# 使用示例

if __name__ == '__main__':
    async def websocket_client():
        uri = 'ws://localhost:12345'  # 服务器地址
        client = WebSocketClient(uri)  # 创建客户端
        async with client:  # 上下文管理器启动客户端

            # 这段注释的代码可以解注后运行，用于测试
            # async def periodic_send():  # 一个测试，每隔一秒发送一条消息
            #     while True:
            #         await client.send("Client message")  # 发送消息
            #         await asyncio.sleep(1)  # 等待一秒
            # asyncio.create_task(periodic_send())  # 启动发送消息的任务

            async def listen():  # 监听服务器返回的消息
                while client:
                    await client.recv()  # 接收消息

            asyncio.create_task(listen())  # 启动监听任务
            await asyncio.Future()  # 保持运行

    # 启动客户端
    asyncio.run(websocket_client())
