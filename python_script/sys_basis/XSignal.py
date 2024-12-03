
class XSignal(object):
    def __init__(self):
        self.__slots = []

    @property
    def slots(self):
        return self.__slots

    def connect(self, slot):
        """连接信号到槽"""
        if callable(slot):
            self.__slots.append(slot)
        else:
            raise ValueError("Slot must be callable")

    def disconnect(self, slot):
        """断开信号与槽的连接"""
        if slot in self.__slots:
            self.__slots.remove(slot)

    def emit(self, *args, **kwargs):
        """发射信号，调用所有连接的槽"""
        for slot in self.__slots:
            slot(*args, **kwargs)
