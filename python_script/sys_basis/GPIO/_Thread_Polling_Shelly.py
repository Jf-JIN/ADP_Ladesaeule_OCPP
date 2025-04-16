from __future__ import annotations
from threading import Thread
import time
import requests
from const.GPIO_Parameter import *
from const.Const_Parameter import *

if 0:
    from ._GPIO_Manager import GPIOManager
    from ._Charge_Unit import ChargeUnit
    from ._Data_Collector import DataCollector
    from ._Shelly import Shelly


_log = Log.SHELLY


class PollingShelly(Thread):
    def __init__(self, parent: GPIOManager, charge_unit_dict: dict, intervall: int | float, timeout: int | float) -> None:
        super().__init__(name='PollingShelly')
        self.__parent: GPIOManager = parent
        self.__shelly_list: list = []
        for item in charge_unit_dict.values():
            item: ChargeUnit
            self.__shelly_list.append(item.shelly)
        self.__shelly_quantity: int = len(self.__shelly_list)
        self.__interval: int | float = intervall
        self.__timeout: int | float = timeout
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__isRunning: bool = True
        self.__current_index: int = 0
        self.__retry_count: int = 0
        self.__max_retry_count: int = GPIOParams.MAX_SHELLY_RETRY

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def __parse_data_json(self, data: dict) -> dict:
        """ EM{
                "id":0,
                "a_current":0.028,
                "a_voltage":234.1,
                "a_act_power":0.0,
                "a_aprt_power":6.6,
                "a_pf":0.00,
                "a_freq":50.0,

                "b_current":0.027,
                "b_voltage":234.2,
                "b_act_power":0.0,
                "b_aprt_power":6.2,
                "b_pf":0.00,
                "b_freq":50.0,

                "c_current":0.027,
                "c_voltage":234.9,
                "c_act_power":0.0,
                "c_aprt_power":6.4,
                "c_pf":0.00,
                "c_freq":50.0,

                "n_current":null,
                "total_current":0.082,
                "total_act_power":0.000,
                "total_aprt_power":19.245, 
                "user_calibrated_phase":[]}
        """
        container: dict = {
            0: {
                'power': data['a_act_power'],
                'pf': data['a_pf'],
                'current': data['a_current'],
                'voltage': data['a_voltage'],
                'frequncy': data['a_freq'],
                'is_valid': True,
                'total': data['total_act_power']},
            1: {
                'power': data['b_act_power'],
                'pf': data['b_pf'],
                'current': data['b_current'],
                'voltage': data['b_voltage'],
                'frequncy': data['b_freq'],
                'is_valid': True,
                'total': data['total_act_power']},
            2: {
                'power': data['c_act_power'],
                'pf': data['c_pf'],
                'current': data['c_current'],
                'voltage': data['c_voltage'],
                'frequncy': data['c_freq'],
                'is_valid': True,
                'total': data['total_act_power']},
        }
        return container

    def run(self) -> None:
        while self.__isRunning:
            shelly: Shelly = self.__shelly_list[self.__current_index]
            shelly_id = shelly.id
            data_address: str = shelly.data_address
            shelly_data = {}
            try:
                response_data: requests.Response = requests.get(data_address, timeout=self.__timeout)
                response_data.raise_for_status()
                data_dict: dict = response_data.json()
                shelly_data.update(self.__parse_data_json(data_dict))
                shelly_data['is_valid'] = shelly_data[0]['is_valid'] and shelly_data[1]['is_valid'] and shelly_data[2]['is_valid']
            except Exception as e:
                if self.__retry_count <= self.__max_retry_count:
                    self.__retry_count += 1
                    time.sleep(self.__interval)
                    continue
                shelly_data = {
                    0: {
                        'power': 0,
                        'pf': 0,
                        'current': 0,
                        'voltage': 0,
                        'frequncy': 0,
                        'is_valid': False,
                        'total': 0},
                    1: {
                        'power': 0,
                        'pf': 0,
                        'current': 0,
                        'voltage': 0,
                        'frequncy': 0,
                        'is_valid': False,
                        'total': 0},
                    2: {
                        'power': 0,
                        'pf': 0,
                        'current': 0,
                        'voltage': 0,
                        'frequncy': 0,
                        'is_valid': False,
                        'total': 0},
                    'is_valid': False,
                }
                if isinstance(e, requests.exceptions.ConnectionError):
                    _log.error(f'Shelly is not connected: {e}')
                else:
                    _log.exception('Shelly read exception')
            shelly.set_data(shelly_data)
            # self.__data_collector.set_shelly_data(shelly_id, shelly_data)
            self.__current_index = (self.__current_index + 1) % self.__shelly_quantity
            time.sleep(self.__interval)

    def stop(self, ) -> None:
        self.__isRunning = False
        self.join()
