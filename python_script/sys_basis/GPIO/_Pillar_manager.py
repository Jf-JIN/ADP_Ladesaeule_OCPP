from _EVSE_manager import EVSEManager
from _Shelly_manager import ShellyManager
from const.GPIO_Parameter import *
from sys_basis.XSignal  import XSignal
import threading

charging_plan = {
    'evseId': 1,
    'chargingProfile': {
        'id': 1,
        'stackLevel': 1,
        'chargingProfilePurpose': 'TxProfile',
        'chargingProfileKind': 'Absolute',
        'chargingSchedule':
            [
                {'id': 1,
                 'chargingRateUnit': 'A',
                 'chargingSchedulePeriod': [
                     {'startPeriod': 0, 'limit': 8.9},
                     {'startPeriod': 2, 'limit': 8.9},
                     {'startPeriod': 4, 'limit': 8.9},
                     {'startPeriod': 6, 'limit': 8.9},
                     {'startPeriod': 8, 'limit': 8.9},
                     {'startPeriod': 10, 'limit': 8.9},
                     {'startPeriod': 12, 'limit': 8.9},
                     {'startPeriod': 14, 'limit': 8.9},
                     {'startPeriod': 16, 'limit': 8.9}
                 ],
                 'startSchedule': '2025-01-15T15:12:20Z'}
            ]
    },
    'customData': None}


class PillarManager:
    def __init__(self,RCD: bool, evse_id: int, client,):
        self.evse = EVSEManager(RCD = RCD, evse_id = evse_id, client = client)
        self.shelly = ShellyManager(evse_id = evse_id)
        self.__charging_plan = {}
        self.__unit = None
        self.__voltage_max = GPIOParams.MAX_VOLTAGE
        self.__evse_id = evse_id
        self.__target_energy = None
        self.__depart_time = None
        self.__current_periode = [0, 0]
        self.__request_periode = 5
        self.__init_signal()
        self.__init_signal_connections()

        self.__Pillar_data_dict = {
            'evse':{},
            'shelly':{}
        }

    @property
    def signal_pillar_regular_adjust_charging_plan(self):
        return self.__signal_Pillar_regular_adjust_charging_plan

    @property
    def signal_pillar_data_for_display(self):
        return self.__signal_Pillar_data_for_display

    @property
    def signal_Pillar_EVSE_ready(self):
        return self.__signal_Pillar_EVSE_ready

    @property
    def signal_Pillar_EVSE_failure(self):
        return self.__signal_Pillar_EVSE_failure

    @property
    def signal_Pillar_shelly_error(self):
        return self.__signal_Pillar_shelly_error

    @property
    def signal_Pillar_vehicle_departed(self):
        return self.__signal_Pillar_vehicle_departed

    @property
    def signal_EVSE_read_write_error(self):
        return self.__signal_EVSE_read_write_error

    def __init_signal(self):
        self.__signal_Pillar_regular_adjust_charging_plan = XSignal()
        self.__signal_Pillar_data_for_display = XSignal()
        self.__signal_Pillar_EVSE_ready = XSignal()
        self.__signal_Pillar_EVSE_failure = XSignal()
        self.__signal_Pillar_vehicle_departed = XSignal()
        self.__signal_EVSE_read_write_error = XSignal()
        self.__signal_Pillar_shelly_error = XSignal()

    def __init_signal_connections(self):
        self.evse.signal_EVSE_ready_to_go.connect(self.signal_Pillar_EVSE_ready)
        # 其他信号连接
        self.evse.signal_EVSE_failure.connect(self.signal_Pillar_EVSE_failure.emit)
        self.evse.send_EVSE_read_write_error.connect(self.signal_EVSE_read_write_error.emit)
        self.evse.signal_vehicle_departed.connect(self.signal_Pillar_vehicle_departed)
        self.shelly.signal_Shelly_data.connect(self.__update_shelly_data)
        self.shelly.signal_Shelly_error.connect(self.signal_Pillar_shelly_error.emit)


    def __update_evse_data(self, data):
        self.__Pillar_data_dict['evse'] = data

    def __update_shelly_data(self, data):
        self.__Pillar_data_dict['shelly'] = data

    def set_charging_profile(self, charging_plan: dict, target_energy: int | float | None = None, depart_time: str | None = None):

        self.__charging_plan = charging_plan
        self.__unit = charging_plan['chargingProfile']['chargingSchedule'][0]['chargingRateUnit']

        if target_energy is not None and depart_time is not None:
            self.shelly.reset_total()
            self.__target_energy = target_energy
            self.__depart_time = depart_time

        self.periodic_timer(charging_plan = charging_plan,current_periode=self.__current_periode)


    def get_limit_value(self, charging_plan: dict):
        if self.__unit == 'W':
            return charging_plan['limit'] / self.__voltage_max
        else:
            return charging_plan['limit']


    def periodic_timer(self, charging_plan, current_periode: list):

        if len(charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']) <= 0:
            self.evse.turn_off_charging_now()
            return
        current_plan = self.__charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'].pop(0)
        # print(current_plan)
        interval = (current_plan['startPeriod'] - current_periode[0]) * 60
        limit = self.get_limit_value(current_plan)
        self.evse.set_current(limit)
        current_periode[0] = current_plan['startPeriod']  # current_periode += interval
        if current_periode[0] // self.__request_periode >= current_periode[1]:
            if current_periode[1] != 0:
                # 加字典保护和只发送需要信息，改个新的信号
                remained_to_charge = []
                remained_to_charge[0] = self.__evse_id
                remained_to_charge[1] = self.__target_energy - self.shelly.charged_energy()

                self.pillar_regular_adjust_charging_plan.emit(remained_to_charge)
            current_periode[1] = current_periode[0] // self.__request_periode
        self.__timer = threading.Timer(interval, self.periodic_timer, [charging_plan,current_periode, ])
        self.__timer.start()  # init 设置timer none
