from __future__ import annotations
import asyncio

from sys_basis.Ports import *
from const.Const_Parameter import *

_log = Log.RAS


class ManagerCoroutines(object):
    def __init__(self, *task_obj):
        self.__task_obj_tuple = task_obj

    async def __load_tasks(self) -> None:
        tasks = [task_func.run() for task_func in self.__task_obj_tuple]
        await asyncio.gather(*tasks)

    def start(self) -> None:
        asyncio.run(self.__load_tasks())

    # def stop(self) -> None:
    #     for task_obj in self.__task_obj_tuple:
    #         task_obj: PortOCPPWebsocketClient | PortWebSocketServer
    #         task_obj.stop()

    def stop(self) -> None:
        self.__isRunning = False
        for task in self.__task_obj_tuple:
            if task:
                task.stop()
                task = None
                # asyncio.ensure_future(self.__await_task_silently(task))

    # @staticmethod
    # async def __await_task_silently(task: asyncio.Task) -> None:
    #     try:
    #         await task
    #     except Exception as e:
    #         _log.exception()

    def __del__(self) -> None:
        self.stop()
