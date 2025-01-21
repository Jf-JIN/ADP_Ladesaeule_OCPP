import time
from threading import Thread
from sys_basis.GPIO._evse_r_w import EVSEReadWrite
from sys_basis.XSignal  import XSignal
from const.GPIO_Parameter import *
from _Decorator_check_flag import check_flag


class ThreadWaitForEV(Thread):

    def __init__(self, polling_interval,client,evse_id):
        super().__init__()
        self.__polling_interval = polling_interval
        self.__isRunning = True
        self.__signal_finished = XSignal()
        self.__signal_info = XSignal()
        self.__signal_transfer_data = XSignal()
        self.__signal_EV_is_present = XSignal()
        self.read = EVSEReadWrite(client,evse_id)
        self.__vehicle_state = None

    @property
    def signal_info(self):
        return self.__signal_info

    @property
    def signal_EV_is_present(self):
        return self.__signal_EV_is_present

    @property
    def signal_transfer_data(self):
        """转发收到的数据 """
        return self.__signal_transfer_data

    @property
    def signal_finished(self):
        """返回线程完成的信号"""
        return self.__signal_finished


    def run(self):
        """
        轮询循环，每隔一定时间读取寄存器并发送信息
        """
        while self.__isRunning:
            data = self.read.get_vehicle_state()
            flag, value, message = data
            self.signal_transfer_data.emit(data)
            if flag != ResultFlag.FAIL:
                self.__vehicle_state = value[0]
                self.__signal_info.emit("waiting for EV...")
                if self.__vehicle_state == VehicleState.EV_IS_PRESENT:
                    self.__signal_info.emit("EV is present")
                    self.signal_EV_is_present.emit()

            time.sleep(self.__polling_interval)  # 等待指定的轮询间隔
        self.signal_finished.emit()  # 发送完成信号


    def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束