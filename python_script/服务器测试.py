import asyncio
import time
from sys_basis.Ports.Port_WebSocket_Server import WebSocketServer
from ocpp.routing import on
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.Charge_Point import ChargePointV201
from sys_basis.Ports.Server_Web_Charge_Point import ServerWeb


class MyChargePoint_S(ChargePointV201):
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
    server = WebSocketServer('localhost', 12346)
    server.signal_websocket_server_recv.connect(out)
    charge_point = MyChargePoint_S('CP1', server, 10)
    async with server:

        async def send_boot_notification():
            while True:
                await asyncio.sleep(10)
                await charge_point.send_request_message(authorize_request.generate(
                    id_token=authorize_request.get_id_tocken('111', type='Central'),
                    custom_data=authorize_request.get_custom_data(str(time.time()))))

        task = asyncio.create_task(charge_point.start())
        send_task = asyncio.create_task(send_boot_notification())
        # await asyncio.gather(task, send_task)
        await asyncio.gather(send_task)

        await asyncio.Future()


def out(message):  # 槽函数
    print(f'out\t{message}')


asyncio.run(start_server())

a = ServerWeb()
a.start()
