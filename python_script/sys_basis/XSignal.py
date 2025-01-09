import asyncio


class XSignal(object):
    def __init__(self, type_=None):
        self.__type_ = type_ if type(type_) == type else None
        self.__slots = []
        self.__aslots = []

    def connect(self, slot):
        """
        连接信号到槽
        """
        if callable(slot):
            if slot not in self.__slots:
                self.__slots.append(slot)
        else:
            raise ValueError("Slot must be callable")

    def aconnect(self, slot):
        """
        异步连接信号到槽
        """
        if callable(slot):
            if slot not in self.__aslots:
                self.__aslots.append(slot)
        else:
            raise ValueError("Slot must be callable")

    def disconnect(self, slot):
        """
        断开信号与槽的连接
        """
        if slot in self.__slots:
            self.__slots.remove(slot)

    def adisconnect(self, slot):
        """
        异步断开信号与槽的连接
        """
        if slot in self.__aslots:
            self.__aslots.remove(slot)

    def emit(self, *args, **kwargs):
        """
        发射信号, 调用所有连接的槽
        """
        if self.__type_ is not None:
            if len(args) != 1 or not isinstance(args[0], self.__type_):
                raise TypeError(f"Signal type mismatch, it schould be {self.__type_.__name__}, but got {type(args[0])}")
        for slot in self.__slots:
            slot(*args, **kwargs)

    async def aemit(self, *args, **kwargs):
        """
        异步发射信号, 调用所有连接的异步槽
        """
        tasks = []
        for slot in self.__aslots:
            if asyncio.iscoroutinefunction(slot):  # 异步槽函数
                tasks.append(slot(*args, **kwargs))
            else:  # 同步槽函数
                slot(*args, **kwargs)

        if tasks:  # 等待异步任务完成
            await asyncio.gather(*tasks)
