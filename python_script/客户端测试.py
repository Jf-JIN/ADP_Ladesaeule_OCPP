import asyncio
import time
from sys_basis.WebSocket_Client import WebSocketClient
from ocpp.v201 import ChargePoint
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *


class MyChargePoint(ChargePoint):
    async def send_boot_notification(self):
        boot_notification = authorize_request.generate(
            id_token=authorize_request.get_id_tocken('111', type='Central'),
            custom_data=authorize_request.get_custom_data(str(time.time()))
        )
        # a = {"idToken": "111", "type": "Central"}
        # boot_notification = authorize_request.generate(a)
        print("\nSending BootNotification:", boot_notification)

        try:
            response = await self.call(boot_notification)
            print('\n->Response received 芜湖!>:', repr(response))
        except asyncio.TimeoutError:
            print("\nRequest timed out.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")


async def main():
    uri = 'ws://localhost:12345'
    client = WebSocketClient(uri)
    charge_point = MyChargePoint('CP1', client)
    async with client:
        async def listen_for_messages():
            while True:
                message = await client.recv()
                print("Received message from server:", message)
                if message is not None and isinstance(message, str) and message.startswith('['):
                    await charge_point.route_message(message)

        listening_task = asyncio.create_task(listen_for_messages())
        await charge_point.send_boot_notification()
        await charge_point.send_boot_notification()
        await asyncio.gather(listening_task)

        await asyncio.Future()

asyncio.run(main())
