
import asyncio


class ManagerCoroutines(object):
    def __init__(self, *task_func):
        self.__tasks = task_func

    async def __load_tasks(self) -> None:
        tasks = [task_func() for task_func in self.__tasks]
        await asyncio.gather(*tasks)

    def start(self) -> None:
        asyncio.run(self.__load_tasks())
