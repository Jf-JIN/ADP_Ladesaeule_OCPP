import asyncio
from urllib import response
from sys_basis.WebSocket_Server import WebSocketServer
from ocpp.routing import on
from ocpp.v201 import ChargePoint, call
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *


class MyChargePoint(ChargePoint):
    @on('Authorize')
    async def on_authorize_request(self, id_token: dict):
        print(f'Received AuthorizeRequest from {id_token}\n')
        response_obj = authorize_response.generate(
            authorize_response.get_id_token_info('Accepted'),
        )
        return response_obj


async def start_server():
    server = WebSocketServer('localhost', 12345)
    server.signal_recv.connect(out)
    charge_point = MyChargePoint('CP1', server)
    async with server:
        await charge_point.start()
        await asyncio.Future()


def out(message):  # 槽函数
    print(f'out\t{message}')


loop = asyncio.get_event_loop()
server = loop.run_until_complete(start_server())

# 运行事件循环
loop.run_forever()
