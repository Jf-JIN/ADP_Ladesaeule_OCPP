from __future__ import annotations
import asyncio

from sys_basis.Ports import *


class ManagerCoroutines(object):
    def __init__(self, *task_obj):
        self.__task_obj_tuple = task_obj

    async def __load_tasks(self) -> None:
        tasks = [task_func.run() for task_func in self.__task_obj_tuple]
        await asyncio.gather(*tasks)

    def start(self) -> None:
        asyncio.run(self.__load_tasks())

    def stop(self) -> None:
        for task_obj in self.__task_obj_tuple:
            task_obj: PortOCPPWebsocketClient | PortWebSocketServer
            task_obj.close()

    def __del__(self) -> None:
        self.stop()
