

import csv
import time

from const.Const_Parameter import *
from const.GPIO_Parameter import *
from tools.data_gene import *

_log = Log.CSVWriter


class ShellyDataCSVWriter:
    def __init__(self, cu_id: int):
        self.__cu_id: int = cu_id
        self.__root_dir: str = APP_WORKSPACE_PATH
        self.__root_folder_name: str = 'Data'
        self.__csv_folder_name: str = f'ChargeUnit_ID{self.__cu_id}'
        self.__csv_file_dir: str = os.path.join(self.__root_dir, self.__root_folder_name, self.__csv_folder_name)
        self.__csv_file_path_list: list = []
        self.__last_calculation_time = time.time()
        self.__thread_lock = threading.Lock()
        self.__thread_write = threading.Thread(target=self.__write_csv_file)
        self.__init_parameters()

    @property
    def cvs_file_path_list(self) -> list:
        if not self.__csv_file_path_list:
            res = os.listdir(self.__csv_file_dir)
            self.__csv_file_path_list = [f for f in res if f.endswith('.csv')]
        return self.__csv_file_path_list

    @property
    def current_csv_file_name(self) -> str:
        return f"Data_ID{self.__cu_id}_{self.__start_time}.csv"

    @property
    def current_csv_file_path(self):
        return os.path.join(self.__csv_file_dir, self.current_csv_file_name)

    def write_shelly_data(self, current_list: list, voltage_list: list, power_list: list, energy_list: list, shelly_total_energy: int, actual_calculate_energy):
        if not self.__isSmartCharging:
            return
        if len(current_list) != 3 or len(voltage_list) != 3 or len(power_list) != 3 or len(energy_list) != 3:
            raise ValueError("The length of the list must be 3")
        current_time: str = DataGene.getCurrentTime()
        total_calculated_energy = self.__get_current_calculated_charged_energy()
        action_limit = self.__current_action.get('limit', -1)
        action_periode = self.__current_action.get('startPeriod', -1)
        data: list = [
            current_time,
            *current_list, *voltage_list, *power_list, *energy_list,
            shelly_total_energy, actual_calculate_energy, total_calculated_energy,
            action_periode, action_limit, self.__value_unit]
        with open(self.current_csv_file_path, 'a') as f:
            f.write(','.join([str(i) for i in data]) + '\n')

    def stop_writing(self):
        self.__set_enable_charge(False)
        self.__init_parameters()

    def start_writing(self):
        if self.__isSmartCharging:
            _log.info(f'There is already a writer(id: {self.__cu_id}) running, please stop it first')
            return
        self.__set_enable_charge(True)

    def set_current_action(self, plan: dict, value_unit='W'):
        if not self.__isSmartCharging:
            return
        self.__current_action = plan
        self.__value_unit: str = value_unit

    def __init_parameters(self):
        self.__current_action: dict = {
            'limit': 0,
            'startPeriod': 0,
        }
        self.__value_unit = 'W'
        self.__total_charged_energy: int = 0
        self.__isSmartCharging = False

    def __set_enable_charge(self, enable: bool):
        self.__isSmartCharging: bool = enable

    def __set_start_charging_time(self, start_time: str):
        self.__start_time = start_time

    def __convert_value_in_walt(self, charging_limit: int) -> int:
        if self.__value_unit in ['W', 'w']:
            return charging_limit
        elif self.__value_unit in ['A', 'a']:
            return charging_limit * GPIOParams.MAX_VOLTAGE
        else:
            raise ValueError(f'Value unit {self.__value_unit} is not supported')

    def __get_current_calculated_charged_energy(self) -> int:
        current_time: float = time.time()
        diff_time: float = current_time - self.__last_calculation_time / 3600  # Unit h
        norm_power = self.__convert_value_in_walt(self.__current_action.get('limit', 0))
        self.__total_charged_energy += diff_time * norm_power  # Unit Wh
        return self.__total_charged_energy

    def __write_in_loop(self):
        while self.__isSmartCharging:
            ...
