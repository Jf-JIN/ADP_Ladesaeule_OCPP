

import csv
from const.Const_Parameter import *


class ShellyDataCVSWriter:
    def __init__(self, cu_id: int):
        self.__cu_id = cu_id
        self.__root_path =
        self.__start_time = '00-00-00T00:00:00Z'
        self.__csv_file_path = f"ID{self.__cu_id}_{self.__start_time}data.csv"

    @property
    def cvs_file_path_list(self):
        ...

    def write_shelly_data(self, data: list):
        ...

    def stop_writing(self):
        ...

    def start_writing(self):
        ...

    def set_current_action(self, plan: dict, value_unit='W'):
        ...

    def __set_enable_charge(self, enable: bool):
        ...

    def __set_start_charging_time(self, start_time: str):
        self.__start_time = start_time
