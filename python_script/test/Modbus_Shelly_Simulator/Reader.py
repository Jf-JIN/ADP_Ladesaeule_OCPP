
import json
from PyQt5.QtCore import pyqtSignal, QThread, QTimer


class ReaderThread(QThread):
    """ 
    读取文件线程
    """

    signal_reader = pyqtSignal(dict, bool)

    def __init__(self, file_path) -> None:
        super().__init__()
        self.__file_path = file_path
        self.__evse_state_1007 = 0
        self.__vehicle_state_1002 = 1
        self.__current_max_1003 = 6
        self.__current_min_2002 = 5
        self.__onoff_selftest_1004 = 0
        self.__configured_amps_1000 = 0
        self.__charge_operation_2005 = 0b001001
        self.__latch_lock_pin = ''
        self.__latch_unlock_pin = ''
        self.__max_voltage = 230
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.read_json)
        self.__timer.start(100)
        self.__file_lock = True
        self.__isSuccess = True
        self.running = True

    def file_lock(self):
        return self.__file_lock

    def read_json(self):
        try:
            self.__file_lock = True
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data: dict = json.load(f)
                evse_state_1007 = int(data.get('1007', 0))
                vehicle_state_1002 = int(data.get('1002', 1))
                current_max_1003 = int(data.get('1003', 6))
                current_min_2002 = int(data.get('2002', 5))
                onoff_selftest_1004 = int(data.get('1004', 0))
                configured_amps_1000 = int(data.get('1000', 0))
                charge_operation_2005 = int(data.get('2005', 0))
                latch_lock_pin = data.get('latch_lock_pin', None)
                latch_unlock_pin = data.get('latch_unlock_pin', None)
                max_voltage = int(data.get('max_voltage', 230))
                if isinstance(latch_lock_pin, (int, float)):
                    if latch_lock_pin > 0:
                        latch_lock_pin = 1
                    else:
                        latch_lock_pin = 0
                if isinstance(latch_unlock_pin, (int, float)):
                    if latch_unlock_pin > 0:
                        latch_unlock_pin = 1
                    else:
                        latch_unlock_pin = 0
            self.__file_lock = False
            self.__isSuccess = True
        except:
            self.__file_lock = False
            self.__isSuccess = False
            evse_state_1007 = self.__evse_state_1007
            vehicle_state_1002 = self.__vehicle_state_1002
            current_max_1003 = self.__current_max_1003
            current_min_2002 = self.__current_min_2002
            onoff_selftest_1004 = -1
            configured_amps_1000 = -1
            charge_operation_2005 = -1
            latch_lock_pin = 'Error'
            latch_unlock_pin = 'Error'
            max_voltage = self.__max_voltage
        if (
            evse_state_1007 != self.__evse_state_1007
            or vehicle_state_1002 != self.__vehicle_state_1002
            or current_max_1003 != self.__current_max_1003
            or current_min_2002 != self.__current_min_2002
            or onoff_selftest_1004 != self.__onoff_selftest_1004
            or configured_amps_1000 != self.__configured_amps_1000
            or charge_operation_2005 != self.__charge_operation_2005
            or latch_lock_pin != self.__latch_lock_pin
            or latch_unlock_pin != self.__latch_unlock_pin
            or max_voltage != self.__max_voltage
        ):
            temp: dict = {
                '1007': evse_state_1007,
                '1002': vehicle_state_1002,
                '1003': current_max_1003,
                '2002': current_min_2002,
                '1004': onoff_selftest_1004,
                '1000': configured_amps_1000,
                '2005': charge_operation_2005,
                'latch_lock_pin': latch_lock_pin,
                'latch_unlock_pin': latch_unlock_pin,
                'max_voltage': max_voltage,

            }
            self.__evse_state_1007 = evse_state_1007
            self.__vehicle_state_1002 = vehicle_state_1002
            self.__current_max_1003 = current_max_1003
            self.__current_min_2002 = current_min_2002
            self.__onoff_selftest_1004 = onoff_selftest_1004
            self.__configured_amps_1000 = configured_amps_1000
            self.__charge_operation_2005 = charge_operation_2005
            self.__latch_lock_pin = latch_lock_pin
            self.__latch_unlock_pin = latch_unlock_pin
            self.signal_reader.emit(temp, self.__isSuccess)
