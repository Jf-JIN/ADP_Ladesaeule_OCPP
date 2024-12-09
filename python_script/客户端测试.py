import asyncio
from sys_basis.WebSocket_Client import WebSocketClient
from ocpp.v201 import ChargePoint, call
from datetime import datetime
from sys_basis.Generator_Ocpp_Std.V2_0_1 import authorize_request


# 自定义ChargePoint类, 发送 BootNotification 消息
class MyChargePoint(ChargePoint):
    async def send_boot_notification(self):
        boot_notification = authorize_request.generate(id_token=authorize_request.get_id_tocken('ddd', type='Central'))

        # 调用 `self.call` 并发送消息
        response = await self.call(boot_notification)


# WebSocket 客户端连接并发送 BootNotification 消息
async def main():
    uri = 'ws://localhost:12345'  # 服务器地址
    client = WebSocketClient(uri)
    charge_point = MyChargePoint('CP1', client)
    async with client:
        await client.send('Hello, World!')
        # while client:
        #     await client.recieve()

        await charge_point.send_boot_notification()  # 发送消息
        await client.recv()
        await asyncio.Future()

asyncio.run(main())
