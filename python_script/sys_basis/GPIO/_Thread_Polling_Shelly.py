
from threading import Thread
import time
import requests
from const.GPIO_Parameter import *
from const.Const_Parameter import *

if 0:
    from ._GPIO_Manager import GPIOManager
    from ._Data_Collector import DataCollector
    from ._Shelly import Shelly


_exception = Log.SHELLY.exception


class PollingShelly(Thread):
    def __init__(self, parent: GPIOManager, *, charge_unit_dict: dict, intervall: int | float, timeout: int | float) -> None:
        super().__init__()
        self.__parent: GPIOManager = parent
        self.__shelly_list: list = []
        for item in charge_unit_dict.values():
            self.__shelly_list.append(item['shelly'])
        self.__shelly_quantity: int = len(self.__shelly_list)
        self.__interval: int | float = intervall
        self.__timeout: int | float = timeout
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__isRunning: bool = True
        self.__current_index: int = 0

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def run(self) -> None:
        while self.__isRunning:
            shelly: Shelly = self.__shelly_list[self.__current_index]
            shelly_id = shelly.id
            sub_url0: str = shelly.sub_address_0
            sub_url1: str = shelly.sub_address_1
            sub_url2: str = shelly.sub_address_2
            shelly_data = {}
            try:
                response_0: requests.Response = requests.get(sub_url0, timeout=self.__timeout)
                response_0.raise_for_status()
                data_0: dict = response_0.json()
                shelly_data[0] = data_0

                response_1: requests.Response = requests.get(sub_url1, timeout=self.__timeout)
                response_1.raise_for_status()
                data_1: dict = response_1.json()
                shelly_data[1] = data_1

                response_2: requests.Response = requests.get(sub_url2, timeout=self.__timeout)
                response_2.raise_for_status()
                data_2: dict = response_2.json()
                shelly_data[2] = data_2
                """ 
                {
                "power": 0,
                "pf": 0,
                "current": 0,
                "voltage": 0,
                "is_valid": true,
                "total": 0,
                "total_returned": 0
                }
                """
                shelly_data['charged_energy'] = data_0['total'] + data_1['total'] + data_2['total']
                shelly_data['return_energy'] = data_0['total_returned'] + data_1['total_returned'] + data_2['total_returned']
                shelly_data['is_valid'] = data_0['is_valid'] and data_1['is_valid'] and data_2['is_valid']
                shelly.set_data(shelly_data)
                self.__data_collector.set_shelly_data(shelly_id, shelly_data)
            except Exception as e:
                _exception(f'Shelly read exception: {e}')
            self.__current_index = (self.__current_index + 1) % self.__shelly_quantity
            time.sleep(self.__interval)

    def stop(self, ) -> None:
        self.__isRunning = False
        self.join()
