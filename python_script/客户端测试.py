import asyncio
from sys_basis.WebSocket_Client import WebSocketClient
from ocpp.v201 import ChargePoint, call
from datetime import datetime
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *


# 自定义ChargePoint类, 发送 BootNotification 消息
class MyChargePoint(ChargePoint):
    async def send_boot_notification(self):
        boot_notification = authorize_request.generate(id_token=authorize_request.get_id_tocken('ddd', type='Central'))

        print('Sending BootNotification:', boot_notification)

        try:
            response = await self.call(boot_notification)
            print('->Response received>:', repr(response))
        except asyncio.TimeoutError:
            print('Request timed out.')
        except Exception as e:
            print(f'An error occurred: {e}')


# WebSocket 客户端连接并发送 BootNotification 消息
async def main():
    uri = 'ws://localhost:12345'  # 服务器地址
    client = WebSocketClient(uri)
    charge_point = MyChargePoint('CP1', client)
    async with client:
        # async def listening():
        #     while client:
        #         await client.recv()

        # await charge_point.send_boot_notification()  # 发送消息
        # await asyncio.create_task(listening())
        # await asyncio.create_task(await charge_point.send_boot_notification())

        async def listen_for_messages():
            while True:  # 持续接收消息
                message = await client.recv()
                print('Received message from server:', message)

        listening_task = asyncio.create_task(listen_for_messages())
        await charge_point.send_boot_notification()
        await asyncio.gather(listening_task)  # 等待监听任务

        # await charge_point.send_boot_notification()
        await asyncio.Future()

asyncio.run(main())
