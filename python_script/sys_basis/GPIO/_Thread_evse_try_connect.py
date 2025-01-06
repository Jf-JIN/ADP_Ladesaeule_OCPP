from threading import Thread
import time
from XSignal import XSignal
from _EVSE_communication import EVSECommunication

class TryConnection(Thread):
    def __init__(self, polling_interval,parent):
        super().__init__()
        self.__parent_obj = parent
        self.__polling_interval = polling_interval
        self.__isRunning = True
        self.__signal_finished = XSignal()
        #self.__evse_communication = EVSECommunication()
        self.__client = self.__parent_obj._client
        self.__send_signal_info = self.__parent_obj.__send_signal_info
        self.__signal_internal = XSignal()

    @property
    def signal_internal(self):
        """返回连接状态更新的信号"""
        return self.__signal_internal

    @property
    def signal_finished(self):
        """返回线程完成的信号"""
        return self.__signal_finished

    def run(self):
        """
        轮询循环，每隔一定时间读取寄存器并发送信息
         """
        while self.__isRunning and not self.checking():
            time.sleep(self.__polling_interval)  # 等待指定的轮询间隔
        self.signal_finished.emit()  # 发送完成信号

    def checking(self):
        """
        检查EVSE是否连接
        """
        if self.__client.connect():
            self.__send_signal_info(f"重新连接成功")
            self.signal_internal.emit(True)
            return True
        else:
            self.__send_signal_info(f"重新连接失败")
            self.signal_internal.emit(False)
            return False

    def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束