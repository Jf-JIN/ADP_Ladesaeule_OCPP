

import json
from const.Const_Parameter import *
from threading import Event
import time


class ModbusPDU:
    function_code: int = 0
    sub_function_code: int = -1
    rtu_frame_size: int = 0
    rtu_byte_count_pos: int = 0
    exception_code: int = 0
    registers: list = []
    status: int = 0
    dev_id: int = 0
    transaction_id: int = 0
    bits: int = 0
    address: int = 0
    count: int = 0

    ILLEGAL_FUNCTION = 0x01
    ILLEGAL_ADDRESS = 0x02
    ILLEGAL_VALUE = 0x03
    SLAVE_FAILURE = 0x04
    ACKNOWLEDGE = 0x05
    SLAVE_BUSY = 0x06
    NEGATIVE_ACKNOWLEDGE = 0x07
    MEMORY_PARITY_ERROR = 0x08
    GATEWAY_PATH_UNAVIABLE = 0x0A
    GATEWAY_NO_RESPONSE = 0x0B

    def __init__(self, registers=[], *args, **kwargs):
        self.registers = registers if isinstance(registers, list) else [registers]

    @staticmethod
    def isError() -> bool:
        return False

    def validateCount(self, max_count: int, count: int = -1) -> None:
        pass

    def validateAddress(self, address: int = -1) -> None:
        pass

    def get_response_pdu_size(self) -> int:
        return 0


class ModbusSerialClient:
    def __init__(self, *args, **kwargs):
        self.__json_file_path = os.path.join(os.getcwd(), 'test', 'Modbus_Shelly_Simulator.json')
        # print(self.__json_file_path)
        self.__json_dict = {}
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def _in_waiting(self):
        return 0

    def send(self, request: bytes, addr: tuple | None = None) -> int:
        return 0

    def _wait_for_data(self) -> int:
        return 0

    def recv(self, size: int | None) -> bytes:
        return b''

    def is_socket_open(self) -> bool:
        return True

    @property
    def connected(self) -> bool:
        return True

    def read_holding_registers(self,
                               address: int,
                               *,
                               count: int = 1,
                               slave: int = 1,
                               no_response_expected: bool = False):
        address = str(address)
        with open(self.__json_file_path, 'r', encoding='utf-8') as f:
            json_dict = json.load(f)
            if address not in json_dict:
                json_dict[address] = 0
            self.__json_dict = json_dict
            return ModbusPDU(json_dict[address])

    def write_registers(
        self,
        address: int,
        values: list[int],
        *,
        slave: int = 1,
        no_response_expected: bool = False
    ):
        address = str(address)
        with open(self.__json_file_path, 'r', encoding='utf-8') as f:
            self.__json_dict = json.load(f)
        self.__json_dict[address] = values[0]
        with open(self.__json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__json_dict, f, indent=4, ensure_ascii=False)
        return ModbusPDU


class LED:
    def __init__(self, pin):
        if pin == 23:
            self.__key = 'latch_lock_pin'
        elif pin == 22:
            self.__key = 'latch_unlock_pin'
        elif pin == 25:
            self.__key = 'led_pin'
        else:
            self.__key = 'others'
        self.__fp = os.path.join(os.getcwd(), 'test', 'Modbus_Shelly_Simulator.json')

    def on(self):
        with open(self.__fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[self.__key] = 1
        with open(self.__fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def off(self):
        with open(self.__fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[self.__key] = 0
        with open(self.__fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class Button:
    def __init__(self, pin, *args, **kwargs):
        self.__pin = pin
        if pin == 20:
            self.__key = 'start_btn'
        elif pin == 21:
            self.__key = 'stop_btn'
        self.__fp = os.path.join(os.getcwd(), 'test', 'Modbus_Shelly_Simulator.json')

    def when_activated(self):
        ...

    def wait_for_active(self):
        time.sleep(10000000)

    def wait_for_inactive(self):
        time.sleep(10000000)

    @property
    def _active_event(self):
        return Event()


class RPi:
    class _GPIO:
        def setmode(arg):
            ...

        def setup(*args, **kwargs):
            ...

        def add_event_detect(*args, **kwargs):
            ...

    def __init__(self, *args, **kwargs):
        ...

    @staticmethod
    def GPIO():
        return RPi._GPIO
