import time
from threading import Thread
import threading
from const.GPIO_Parameter import *
from sys_basis.XSignal  import XSignal

class ThreadChargeProfile(Thread):
    def __init__(self, charging_plan,evse_instance,shelly_instance,target_energy,depart_time):
        super().__init__()

        self.__voltage_max = GPIOParams.MAX_VOLTAGE
        self.__evse_instance = evse_instance
        self.__shelly_instance = shelly_instance
        self.__charging_plan = charging_plan
        self.__depart_time = depart_time
        self.__unit = charging_plan['chargingProfile']['chargingSchedule'][0]['chargingRateUnit']
        self.__current_periode = [0, 0]
        self.__request_periode = 5
        self.__signal_charging_data = XSignal()
        self.__target_energy = target_energy
        self.__running = True
        self.periodic_timer(self.__current_periode)

    @property
    def signal_charging_data(self):
        return self.__signal_charging_data

    def stop(self):
        self.__running = False

    def get_limit_value(self,charging_plan: dict):
        if self.__unit == 'W':
            return charging_plan['limit'] / self.__voltage_max
        else:
            return charging_plan['limit']

    def periodic_timer(self,current_periode: list):

        if not self.__running:
            return

        if len(self.__charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']) <= 0:
            self.__evse_instance.turn_off_charging_now()
            return
        current_plan = self.__charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'].pop(0)
        # print(current_plan)
        interval = (current_plan['startPeriod'] - current_periode[0])*60
        limit = self.get_limit_value(current_plan)
        self.__evse_instance.set_current(limit)
        current_periode[0] = current_plan['startPeriod']  # current_periode += interval
        if current_periode[0] // self.__request_periode >= current_periode[1]:
            if current_periode[1] != 0:
                #加字典保护和只发送需要信息, 改个新的信号
                data = self.__evse_instance.get_evse_data()
                data['planed_depart_time'] = self.__depart_time
                data['remained_to_charge'] = self.__target_energy - self.__shelly_instance.charged_energy()
                self.signal_charging_data.emit(data)
            current_periode[1] = current_periode[0] // self.__request_periode
        threading.Timer(interval, self.periodic_timer, [current_periode]).start()

