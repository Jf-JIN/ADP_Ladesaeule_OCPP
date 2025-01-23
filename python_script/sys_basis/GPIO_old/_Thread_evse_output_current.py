import time
from threading import Thread
from sys_basis.GPIO._evse_r_w import EVSEReadWrite
from sys_basis.XSignal  import XSignal



class ThreadOutputCurrent(Thread):

    def __init__(self, polling_interval,client,evse_id):
        super().__init__()
        self.__polling_interval = polling_interval
        self.__isRunning = True
        self.__signal_finished = XSignal()
        self.__signal_transfer_data = XSignal()
        self.read = EVSEReadWrite(client,evse_id)
    @property
    def signal_transfer_data(self):
        """转发收到的电流值"""
        return self.__signal_transfer_data

    @property
    def signal_finished(self):
        """返回线程完成的信号"""
        return self.__signal_finished

    def run(self):
        """
        轮询循环, 每隔一定时间读取寄存器并发送信息
        """
        while self.__isRunning:
            self.signal_transfer_data.emit(self.read.get_actual_current())
            time.sleep(self.__polling_interval)  # 等待指定的轮询间隔
        self.signal_finished.emit()  # 发送完成信号

    def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束