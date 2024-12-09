import asyncio


class AsyncTimer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.__task = None
        self.__isActive = False

    @property
    def isActive(self):
        return self.__isActive

    async def _run(self):
        while True:
            await asyncio.sleep(self.interval)
            await self.callback()

    def start(self):
        """启动定时器"""
        self.stop()  # 始终只启动一次
        self.__task = asyncio.create_task(self._run())
        self.__isActive = True

    def stop(self):
        """停止定时器"""
        if self.__task:
            self.__task.cancel()
            self.__isActive = False
