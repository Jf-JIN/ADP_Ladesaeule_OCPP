import asyncio
from urllib import response
from sys_basis.WebSocket_Server import WebSocketServer
from ocpp.routing import on
from ocpp.v201 import ChargePoint, call
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *


class MyChargePoint(ChargePoint):
    # 监听 BootNotification 消息
    @on('Authorize')
    async def on_authorize_request(self, id_token: dict):
        print(f'Received AuthorizeRequest from {id_token}\n')
        response_obj = authorize_response.generate(
            authorize_response.get_id_token_info('Accepted'),
        )
        return response_obj

# 处理WebSocket连接并启动ChargePoint


async def on_connect(websocket):
    charge_point = MyChargePoint('CP1', websocket)
    await charge_point.start()  # 启动ChargePoint, 等待消息

# 启动WebSocket服务器


async def start_server():
    server = WebSocketServer('localhost', 12345)
    server.signal_recv.connect(out)
    async with server:
        await on_connect(server)
        await asyncio.Future()


def out(message):  # 槽函数
    print(f'out\t{message}')


# 创建并运行事件循环
loop = asyncio.get_event_loop()  # 获取事件循环
server = loop.run_until_complete(start_server())  # 启动WebSocket服务器

# 运行事件循环
loop.run_forever()
