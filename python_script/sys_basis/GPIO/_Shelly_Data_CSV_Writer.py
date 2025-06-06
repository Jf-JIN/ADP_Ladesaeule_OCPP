

import csv
import time
import queue
import zipfile

from const.Const_Parameter import *
from const.GPIO_Parameter import *
from tools.data_gene import *
from DToolslib import *

_log = Log.CSVWriter


class _ZipThread(threading.Thread):
    signal_finished = EventSignal()

    def __init__(self, zip_file_path: str, file_paths: list, name: str = 'ZipThread') -> None:
        super().__init__(name=name, daemon=True)
        self.__zip_file_path: str = zip_file_path
        self.__file_paths: list = file_paths

    def __zip_files(self, zip_file_path, file_paths) -> None:
        _log.info(f"Zip files to {zip_file_path}")
        with zipfile.ZipFile(zip_file_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                arcname = os.path.basename(file_path)
                if arcname in zipf.namelist():
                    _log.info(f"{arcname} already in zip, skipping.")
                    continue
                zipf.write(file_path, arcname=arcname)

    def run(self) -> None:
        self.__zip_files(self.__zip_file_path, self.__file_paths)
        self.signal_finished.emit()


class ShellyDataCSVWriter:
    signal_exported_file_path = EventSignal(str)

    def __init__(self, cu_id: int):
        self.__cu_id: int = cu_id
        self.__root_dir: str = APP_WORKSPACE_PATH
        self.__root_folder_name: str = 'Data'
        self.__csv_folder_name: str = f'ChargeUnit_ID_{self.__cu_id}'
        self.__csv_file_dir: str = os.path.join(self.__root_dir, self.__root_folder_name, self.__csv_folder_name)
        os.makedirs(self.__csv_file_dir, exist_ok=True)
        self.__csv_file_path_list: list = []
        self.__file_start_time = ''
        self.__max_csv_file_count: int = 10
        self.__last_calculation_time = time.time()
        self.__isThreadRunning = True
        self.__write_lock = threading.Lock()
        self.__data_lock = threading.Lock()
        self.__to_write_queue = queue.Queue()
        self.__thread_write = threading.Thread(target=self.__write_in_loop, name=f'CSV_Writer_ID_{self.__cu_id}', daemon=True)
        self.__thread_write.start()
        self.__zip_thread = None
        self.__phase_num = 3
        self.__init_parameters()
        self.__init_folder()

    @property
    def csv_file_path_list(self) -> list:
        self.__check_folder()
        return self.__csv_file_path_list

    @property
    def current_csv_file_name(self) -> str:
        return f"Data_ID_{self.__cu_id}_{self.__file_start_time.replace(':', '-')}.csv"

    @property
    def current_csv_file_path(self) -> str:
        return os.path.join(self.__csv_file_dir, self.current_csv_file_name)

    def request_exported_csv_files_path(self, file_num: int) -> None:
        if file_num > len(self.csv_file_path_list) or file_num <= 0:
            raise ValueError(f'file_num should be less than the number of csv files({self.__csv_file_path_list}) and greater than 0')
        if file_num == 1:
            self.signal_exported_file_path.emit(self.current_csv_file_path)
            return
        else:
            self.__zip_file_path = os.path.join(self.__csv_file_dir, f"Data_ID_{self.__cu_id}_{self.__file_start_time}.zip")
            self.__zip_thread = _ZipThread(self.__zip_file_path, self.csv_file_path_list[-file_num:], name=f'zip_thread_ID_{self.__cu_id}')
            self.__zip_thread.signal_finished.emit(self.__thread_zip_finished)
            self.__zip_thread.start()
            return

    def __thread_zip_finished(self) -> None:
        self.signal_exported_file_path.emit(self.__zip_file_path)

    def write_shelly_data(self, current_list: list, voltage_list: list, power_list: list, energy_list: list, shelly_total_energy: int, actual_calculate_energy: int) -> None:
        if not self.__isSmartCharging:
            return
        if len(current_list) != 3 or len(voltage_list) != 3 or len(power_list) != 3 or len(energy_list) != 3:
            raise ValueError("The length of the list must be 3")
        current_time: str = DataGene.getCurrentTime()
        plan_charged_energy = self.__get_current_calculated_charged_energy()
        action_limit = self.__current_action.get('limit', -1)
        action_periode = self.__current_action.get('startPeriod', -1)
        with self.__data_lock:
            data: list = [
                current_time,
                *current_list, *voltage_list, *power_list, *energy_list,
                shelly_total_energy, actual_calculate_energy, plan_charged_energy,
                self.__current_start_time, action_periode, action_limit, self.__value_unit]
        self.__append_msg_in_queue(data)

    def stop_writing(self):
        self.__set_enable_charge(False)
        self.__init_parameters()

    def start_writing(self):
        if self.__isSmartCharging:
            _log.info(f'There is already a writer(id: {self.__cu_id}) running, please stop it first')
            return
        self.__isSmartCharging = True
        self.__file_start_time = DataGene.getCurrentTime()
        self.__plan_charged_energy = self.__calculate_passed_energy()
        self.__csv_file_path_list.append(self.current_csv_file_path)
        self.__check_folder()
        self.__set_enable_charge(True)
        self.__init_table_header()

    def set_charge_plan(self, start_time: str, charge_plan: list):
        with self.__data_lock:
            self.__start_time_str = start_time
            self.__start_time: float = DataGene.str2time(start_time).timestamp()
            self.__charge_plan = charge_plan

    def stop(self) -> None:
        self.__set_enable_charge(False)
        self.__isThreadRunning = False
        self.__append_msg_in_queue(None)

    def set_current_action(self, plan: dict, value_unit: str, phase_num: int, current_start_time: str) -> None:
        if not self.__isSmartCharging:
            return
        if phase_num not in [1, 2, 3]:
            raise ValueError(f'Invalid phase number: {phase_num}')
        with self.__data_lock:
            self.__phase_num: int = phase_num
            self.__current_action = plan
            self.__current_start_time = current_start_time
            self.__value_unit: str = value_unit

    def __check_folder(self):
        if len(self.__csv_file_path_list) >= self.__max_csv_file_count:
            res: list = os.listdir(self.__csv_file_dir)
            res_full_path: list = [os.path.join(self.__csv_file_dir, f) for f in res]
            sorted_list: list = sorted(res_full_path, key=os.path.getctime)
            temp = [f for f in sorted_list if f.endswith('.csv') and not f.startswith('.')]
            self.__csv_file_path_list = temp[-self.__max_csv_file_count:]
            for f in temp[:-self.__max_csv_file_count]:
                try:
                    os.remove(f)
                except:
                    pass

    def __init_folder(self):
        res: list = [os.path.join(self.__csv_file_dir, fn) for fn in os.listdir(self.__csv_file_dir)]
        sorted_list: list = sorted(res, key=os.path.getctime)
        temp = [f for f in sorted_list if f.endswith('.csv') and not f.startswith('.')]
        self.__csv_file_path_list = temp[-self.__max_csv_file_count:]
        for f in temp[:-self.__max_csv_file_count]:
            try:
                os.remove(f)
            except:
                pass

    def __init_parameters(self):
        self.__current_action: dict = {
            'limit': 0,
            'startPeriod': 0,
        }
        self.__value_unit = 'W'
        self.__plan_charged_energy: int = 0
        self.__isSmartCharging = False

    def __init_table_header(self):
        self.__append_msg_in_queue([f'This file is created at {self.__file_start_time}. The Charging plan started at {self.__start_time_str}. ChargeUnit ID: {self.__cu_id}'])
        header = [
            'time',
            'current_a',
            'current_b',
            'current_c',
            'voltage_a',
            'voltage_b',
            'voltage_c',
            'power_a',
            'power_b',
            'power_c',
            'total_energy_a',
            'total_energy_b',
            'total_energy_c',
            'total_energy_shelly',
            'total_energy_calculated',
            'total_energy_desired',
            'current_plan_startTime',
            'action_startPeriod',
            'action_limit',
            'action_value_unit',
        ]
        self.__append_msg_in_queue(header)

    def __append_msg_in_queue(self, msg: list | None) -> None:
        with self.__write_lock:
            self.__to_write_queue.put(msg)

    def __set_enable_charge(self, enable: bool):
        self.__isSmartCharging: bool = enable

    def __convert_value_in_walt(self, charging_limit: int) -> int:
        if self.__value_unit in ['W', 'w']:
            return charging_limit
        elif self.__value_unit in ['A', 'a']:
            return charging_limit * GPIOParams.MAX_VOLTAGE
        else:
            raise ValueError(f'Value unit {self.__value_unit} is not supported')

    def __get_current_calculated_charged_energy(self) -> int:
        current_time: float = time.time()
        diff_time: float = (current_time - self.__last_calculation_time) / 3600  # Unit h
        norm_power = self.__convert_value_in_walt(self.__current_action.get('limit', 0))
        self.__plan_charged_energy += diff_time * norm_power * self.__phase_num  # Unit Wh
        self.__last_calculation_time = current_time
        return self.__plan_charged_energy

    def __write_in_loop(self):
        while self.__isThreadRunning:
            data: list | None = self.__to_write_queue.get()
            if data:
                with open(self.current_csv_file_path, 'a', newline='') as csv_file:
                    f = csv.writer(csv_file)
                    f.writerow(data)

    def __calculate_passed_energy(self) -> int | float:
        self.__last_calculation_time: float = time.time()
        passed_energy = [0]
        period = 0
        last_limit_value = 0
        last_period = 0
        for action in self.__charge_plan:
            cuurent_period = action['startPeriod']
            diff = cuurent_period - period
            period = cuurent_period
            plan_time = self.__start_time + period
            if plan_time <= self.__last_calculation_time:
                limit_value = self.__convert_value_in_walt(action['limit'])
                passed_energy.append(limit_value * diff / 3600 * self.__phase_num)
                last_limit_value = limit_value
                last_period = period
            else:
                passed_energy.pop(-1)
                energy = last_limit_value * (self.__last_calculation_time - (self.__start_time + last_period)) / 3600 * self.__phase_num
                passed_energy.append(energy)
                break
        return sum(passed_energy)
