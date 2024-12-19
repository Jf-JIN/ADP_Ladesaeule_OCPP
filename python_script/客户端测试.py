import asyncio
import time
from sys_basis.Ports.Core_WebSocket.WebSocket_Client import WebSocketClient
from ocpp.v201 import ChargePoint
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.Charge_Point import ChargePointV201
from sys_basis.Ports.Port_OCPP_WebSocket_Client import PortOCPPWebsocketClient


class MyChargePoint(ChargePoint):
    async def send_boot_notification(self):
        boot_notification = authorize_request.generate(
            id_token=authorize_request.get_id_tocken('111', type='Central'),
            custom_data=authorize_request.get_custom_data(str(time.time()))
        )
        # a = {"idToken": "111", "type": "Central"}
        # boot_notification = authorize_request.generate(a)
        print("Sending BootNotification:", boot_notification)

        try:
            response = await self.call(boot_notification)
            print('\n->Response received 芜湖!>:', repr(response))
        except asyncio.TimeoutError:
            print("\nRequest timed out.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")


async def main():
    uri = 'ws://localhost:12346'
    client = WebSocketClient(uri)
    charge_point = ChargePointV201('CP1', client, 10)
    async with client:
        async def listen_for_messages():
            while True:
                print('aa')
                message = await client.recv()
                print("Received message from server:", message)
                if message is not None and isinstance(message, str) and message.startswith('['):
                    await charge_point.route_message(message)

        async def send_boot_notification():
            while True:
                await asyncio.sleep(1)
                print('休眠 1 s')
                await asyncio.sleep(1)
                print('休眠 2 s')
                await asyncio.sleep(1)
                print('休眠 3 s')
                await asyncio.sleep(1)
                print('休眠 4 s')
                await asyncio.sleep(1)
                print('休眠 5 s')
                await client.send('dfdsafsd    fdsjkafldsajkflsajfklsd;jafklds;jfkdlsa;')
                # await charge_point.send_request_message(authorize_request.generate(
                #     id_token=authorize_request.get_id_tocken('111', type='Central'),
                #     custom_data=authorize_request.get_custom_data(str(time.time()))))

        listening_task = asyncio.create_task(listen_for_messages())
        send_task = asyncio.create_task(send_boot_notification())
        await asyncio.gather(listening_task, send_task)
        # await asyncio.gather(send_task)
        await asyncio.Future()

asyncio.run(main())


# a = PortOCPPWebsocketClient('ws://localhost:12345', 'CP1')
# a.start()
