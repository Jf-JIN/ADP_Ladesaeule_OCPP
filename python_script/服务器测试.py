import asyncio
from WebSocket_Server import WebSocketServer
from ocpp.routing import on
from ocpp.v201 import ChargePoint

from ocpp.v16.enums import Action

# 自定义ChargePoint类, 处理接收到的消息


class MyChargePoint(ChargePoint):
    # 监听 BootNotification 消息
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_model, charge_point_vendor):
        print(f"Received BootNotification from {charge_point_model} - {charge_point_vendor}")
        # 返回响应
        return {
            'status': 'Accepted',
            'currentTime': '2024-12-05T12:00:00Z',
            'interval': 10
        }

# 处理WebSocket连接并启动ChargePoint


async def on_connect(websocket):
    charge_point = MyChargePoint('CP1', websocket)
    await charge_point.start()  # 启动ChargePoint, 等待消息

# 启动WebSocket服务器


async def start_server():
    server = WebSocketServer('localhost', 12345)
    server.signal_recv.connect(out)
    async with server:
        await asyncio.Future()


def out(message):  # 槽函数
    print(f'out\t{message}')


# 创建并运行事件循环
loop = asyncio.get_event_loop()  # 获取事件循环
server = loop.run_until_complete(start_server())  # 启动WebSocket服务器

# 运行事件循环
loop.run_forever()
