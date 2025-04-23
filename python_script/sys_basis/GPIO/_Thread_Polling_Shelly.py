from __future__ import annotations
from threading import Thread
import time
import requests
from sympy.physics.units import energy

from const.GPIO_Parameter import *
from const.Const_Parameter import *
from tools.data_gene import DataGene

if 0:
    from ._GPIO_Manager import GPIOManager
    from ._Charge_Unit import ChargeUnit
    from ._Data_Collector import DataCollector
    from ._Shelly import Shelly
    from _Shelly_Data_CSV_Writer import ShellyDataCSVWriter



_log = Log.SHELLY


class PollingShelly(Thread):
    def __init__(self, parent: GPIOManager, charge_unit_dict: dict, intervall: int | float, timeout: int | float) -> None:
        super().__init__(name='PollingShelly')
        self.__parent: GPIOManager = parent
        self.__shelly_list: list = []
        self.__CSV_writer_list: list = []
        for item in charge_unit_dict.values():
            item: ChargeUnit
            self.__shelly_list.append(item.shelly)
            self.__CSV_writer_list.append(item.shelly_writer)
        self.__shelly_quantity: int = len(self.__shelly_list)
        self.__interval: int | float = intervall
        self.__timeout: int | float = timeout
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__isRunning: bool = True
        self.__current_index: int = 0
        self.__retry_count: int = 0
        self.__max_retry_count: int = GPIOParams.MAX_SHELLY_RETRY
        self.__current_shelly_total_energy_minute: str = ''
        self.__total_energy_dict = {}

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
                # 'is_valid': True,
                # 'total': data['total_act_power'],
            },
            1: {
                'power': data['b_act_power'],
                'pf': data['b_pf'],
                'current': data['b_current'],
                'voltage': data['b_voltage'],
                'frequncy': data['b_freq'],
                # 'is_valid': True,
                # 'total': data['total_act_power'],
            },
            2: {
                'power': data['c_act_power'],
                'pf': data['c_pf'],
                'current': data['c_current'],
                'voltage': data['c_voltage'],
                'frequncy': data['c_freq'],
                # 'is_valid': True,
                # 'total': data['total_act_power'],
            },
            'is_valid': True,
        }
        return container

    def __parse_total_energy_data(self, data: dict) -> dict:
        """ 
        {
            'a_total_act_energy': 0.0,
            'a_total_act_ret_energy': 0.0,
            'b_total_act_energy': 0.0,
            'b_total_act_ret_energy': 0.0,
            'c_total_act_energy': 0.0,
            'c_total_act_ret_energy': 0.0,
            'id': 0,
            'total_act': 0.0,
            'total_act_ret': 0.0
        }
        """
        last_min: str = DataGene.getCurrentMinute()
        container = {
            0: {
                'total_energy': data['a_total_act_energy'],
            },
            1: {
                'total_energy': data['b_total_act_energy'],
            },
            2: {
                'total_energy': data['c_total_act_energy'],
            },
            'total_energy': data['total_act'],
            'total_energy_time_min': last_min,
        }
        # self.__total_energy_dict = container
        return container

    def __update_total_energy_data(self, origin_dict, data: dict) -> None:
        if not data:
            return
        for idx in [0, 1, 2]:
            origin_dict[idx]['total_energy'] = data[idx]['total_energy']
        origin_dict['total_energy'] = data['total_energy']
        origin_dict['total_energy_time_min'] = data['total_energy_time_min']

    def run(self) -> None:
        while self.__isRunning:
            shelly: Shelly = self.__shelly_list[self.__current_index]
            CSV_writer: ShellyDataCSVWriter = self.__CSV_writer_list[self.__current_index]
            shelly_id = shelly.id
            data_address: str = shelly.data_address
            total_energy_address: str = shelly.total_energy_address
            shelly_data = {}
            current_minute = DataGene.getCurrentMinute()
            try:
                response_data: requests.Response = requests.get(data_address, timeout=self.__timeout)
                response_data.raise_for_status()
                data_dict: dict = response_data.json()
                shelly_data.update(self.__parse_data_json(data_dict))
                if current_minute != self.__current_shelly_total_energy_minute:
                    response_total_energy: requests.Response = requests.get(total_energy_address, timeout=self.__timeout)
                    response_total_energy.raise_for_status()
                    total_energy_data_dict: dict = response_total_energy.json()
                    self.__total_energy_dict = self.__parse_total_energy_data(total_energy_data_dict)
                    self.__current_shelly_total_energy_minute = current_minute
                self.__update_total_energy_data(shelly_data, self.__total_energy_dict)
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
                        'total_energy': 0
                        # 'is_valid': False,
                        # 'total': 0,
                    },
                    1: {
                        'power': 0,
                        'pf': 0,
                        'current': 0,
                        'voltage': 0,
                        'frequncy': 0,
                        'total_energy': 0
                        # 'is_valid': False,
                        # 'total': 0,
                    },
                    2: {
                        'power': 0,
                        'pf': 0,
                        'current': 0,
                        'voltage': 0,
                        'frequncy': 0,
                        'total_energy': 0
                        # 'is_valid': False,
                        # 'total': 0,
                    },
                    'is_valid': False,
                    'total_energy': 0,
                    'total_energy_time_min': '',
                }
                if isinstance(e, requests.exceptions.ConnectionError):
                    _log.error(f'Shelly is not connected: {e}')
                else:
                    _log.exception('Shelly read exception')
            shelly.set_data(shelly_data)

            current_list = []
            voltage_list = []
            power_list = []
            energy_list = []
            for i in range(3):
                current_list.append(shelly_data[i]['current'])
                voltage_list.append(shelly_data[i]['voltage'])
                power_list.append(shelly_data[i]['power'])
                energy_list.append(shelly_data[i]['total_energy'])
            CSV_writer.write_shelly_data(
                current_list=current_list,
                voltage_list=voltage_list,
                power_list=power_list,
                energy_list=energy_list,
                shelly_total_energy=shelly_data['total_energy'],
                actual_calculate_energy=shelly.data['charged_energy'],
            )
            # self.__data_collector.set_shelly_data(shelly_id, shelly_data)
            self.__current_index = (self.__current_index + 1) % self.__shelly_quantity
            time.sleep(self.__interval)

    def stop(self, ) -> None:
        self.__isRunning = False
        self.join()
