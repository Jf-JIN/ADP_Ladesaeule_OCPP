import asyncio
from sys_basis.WebSocket_Server import WebSocketServer
from ocpp.routing import on
from ocpp.v201 import ChargePoint, call, enums
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.XSignal import XSignal
import inspect
from sys_basis.Charge_Point_Server import ChargePointServerV201
import time


class MyChargePoint_S(ChargePointServerV201):
    pass

    # @on(Action.authorize)
    # async def on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
    #     self._send_signal_info_and_ocpp_message(Action.authorize)
    #     await asyncio.sleep(5)
    #     response_obj = authorize_response.generate(
    #         id_token_info=authorize_response.get_id_token_info('Accepted'),
    #         custom_data=authorize_response.get_custom_data(str(time.time()))
    #     )
    #     return response_obj


async def start_server():
    server = WebSocketServer('localhost', 12345)
    server.signal_recv.connect(out)
    charge_point = MyChargePoint_S('CP1', server, 5)
    charge_point.show_current_message_to_send()
    async with server:
        await charge_point.start()

        await asyncio.Future()


def out(message):  # 槽函数
    print(f'out\t{message}')


loop = asyncio.get_event_loop()
server = loop.run_until_complete(start_server())
loop.run_forever()
