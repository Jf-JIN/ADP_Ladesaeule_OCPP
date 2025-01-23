import threading
import time


class TestTimer():

    def __init__(self,):
        self.__charging_plan = {}
        self.__unit = None
        self.__voltage_max = 220
        self.__evse_id = 1
        self.__target_energy = None
        self.__depart_time = None
        self.__current_periode = [0, 0]
        self.__request_periode = 5

    def set_charging_profile(self, charging_plan: dict, target_energy: int | float | None = None,
                             depart_time: str | None = None):

        self.__charging_plan = charging_plan
        self.__unit = charging_plan['chargingProfile']['chargingSchedule'][0]['chargingRateUnit']

        if target_energy is not None and depart_time is not None:
           # self.shelly.reset_total()
            self.__timer.cancel()
            self.__target_energy = target_energy
            self.__depart_time = depart_time


        self.periodic_timer(charging_plan=self.__charging_plan, current_periode=self.__current_periode)

    def get_limit_value(self,current_plan):
        if self.__unit == 'W':
            return current_plan['limit'] / self.__voltage_max
        else:
            return current_plan['limit']

    def periodic_timer(self, charging_plan: dict, current_periode: list):
        print(charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'])
        if len(charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']) <= 0:
            return
        current_plan = self.__charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'].pop(0)
        print(f'当前计划表{current_plan}')
        interval = (current_plan['startPeriod'] - current_periode[0])
        limit = self.get_limit_value(current_plan)
        print(f'电流设置{limit}')
        current_periode[0] = current_plan['startPeriod']  # current_periode += interval



        self.__timer = threading.Timer(interval, self.periodic_timer, [charging_plan,current_periode])
        self.__timer.start()  # init 设置timer none

charging_plan_1 = {
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

charging_plan_2 = {
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
                     {'startPeriod': 0, 'limit': 5},
                     {'startPeriod': 2, 'limit': 5},
                     {'startPeriod': 4, 'limit': 5},
                     {'startPeriod': 6, 'limit': 5},
                     {'startPeriod': 8, 'limit': 5},
                     {'startPeriod': 10, 'limit': 5},
                     {'startPeriod': 12, 'limit': 5},
                     {'startPeriod': 14, 'limit': 5},
                     {'startPeriod': 16, 'limit': 5}
                 ],
                 'startSchedule': '2025-01-15T15:12:20Z'}
            ]
    },
    'customData': None}

test=TestTimer()
test.set_charging_profile(charging_plan=charging_plan_1)
time.sleep(10)
test.set_charging_profile(charging_plan=charging_plan_2,target_energy=100,depart_time='2025-01-15T15:12:20Z')