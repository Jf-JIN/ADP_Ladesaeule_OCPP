
from pymodbus.pdu.pdu import *
from pymodbus.client import *
from pymodbus.pdu.pdu import ModbusPDU
from const.Const_Logger import *
from const.Const_Modbus import *
import threading
import traceback
import datetime
import typing

_log = Log.MODBUS


class ModbusDataStruct:
    def __init__(self, load_data: ModbusPDU | dict) -> None:
        if isinstance(load_data, dict):
            self.__load_dict(load_data)
        else:
            self.__load_ModbusDataUnit(load_data)

    def __load_dict(self, data_dict: dict):
        self.__ModbusDataUnit = data_dict.get('ModbusDataUnit', None)
        self.__isError = data_dict.get('isError', None)
        self.__exception_code = data_dict.get('exception_code', None)
        self.__function_code: int = data_dict.get('function_code', None)
        self.__dev_id: int = data_dict.get('dev_id', None)
        self.__transaction_id: int = data_dict.get('transaction_id', None)
        self.__bits: list = data_dict.get('bits', None)
        self.__address: int = data_dict.get('address', None)
        self.__registers: list = data_dict.get('registers', None)
        self.__status: int = data_dict.get('status', None)
        self.__bin_value = data_dict.get('bin_value', None)

    def __load_ModbusDataUnit(self, ModbusDataUnit: ModbusPDU):
        self.__ModbusDataUnit: ModbusPDU = ModbusDataUnit
        self.__isError = ModbusDataUnit.isError()
        if self.__isError:
            ModbusDataUnit: ExceptionResponse = ModbusDataUnit
            self.__exception_code: int = ModbusDataUnit.exception_code
        else:
            self.__exception_code = 0
        self.__function_code: int = ModbusDataUnit.function_code
        self.__dev_id: int = ModbusDataUnit.dev_id
        self.__transaction_id: int = ModbusDataUnit.transaction_id
        self.__bits: list = ModbusDataUnit.bits
        self.__address: int = ModbusDataUnit.address
        self.__registers: list = ModbusDataUnit.registers
        self.__status: int = ModbusDataUnit.status
        if len(self.__registers) > 0:
            self.__bin_value: str = f'0b{self.__registers[0]:016b}'
        else:
            self.__bin_value: str = '-'

    @property
    def ModbusDataUnit(self) -> ModbusPDU:
        return self.__ModbusDataUnit

    @property
    def isError(self) -> bool:
        return self.__isError

    @property
    def exception_code(self) -> int:
        return self.__exception_code

    @property
    def function_code(self) -> int:
        return self.__function_code

    @property
    def dev_id(self) -> int:
        return self.__dev_id

    @property
    def transaction_id(self) -> int:
        return self.__transaction_id

    @property
    def bits(self) -> list:
        return self.__bits

    @property
    def address(self) -> int:
        return self.__address

    @property
    def registers(self) -> list:
        return self.__registers

    @property
    def status(self) -> int:
        return self.__status

    @property
    def bin_value(self) -> str:
        return self.__bin_value

    @property
    def ctime(self) -> int:
        return datetime.datetime.now().strftime("%Y.%m.%d|%H:%M:%S.%f")[:-3]

    @property
    def serial_data(self) -> dict:
        return {
            "ModbusDataUnit": self.__ModbusDataUnit,
            "isError": self.__isError,
            "exception_code": self.__exception_code,
            "function_code": self.__function_code,
            "dev_id": self.__dev_id,
            "transaction_id": self.__transaction_id,
            "bits": self.__bits,
            "address": self.__address,
            "registers": self.__registers,
            "status": self.__status,
            "ctime": self.ctime,
            "bin_value": self.__bin_value
        }

    @property
    def json_data(self) -> dict:
        return {
            "ModbusDataUnit": None,
            "isError": self.__isError,
            "exception_code": self.__exception_code,
            "function_code": self.__function_code,
            "dev_id": self.__dev_id,
            "transaction_id": self.__transaction_id,
            "bits": self.__bits,
            "address": self.__address,
            "registers": self.__registers,
            "status": self.__status,
            "ctime": self.ctime,
            "bin_value": self.__bin_value
        }

    def __repr__(self) -> str:
        return f'''\
ModbusHandler(
registers: "{self.__registers}" ,
function_code: "{self.__function_code}" ,
isError: "{self.__isError}" ,
exception_code: "{self.__exception_code}" ,
status: "{self.__status}" ,
dev_id: "{self.__dev_id}" ,
transaction_id: "{self.__transaction_id}" ,
bits: "{self.__bits}" ,
address: "{self.__address}" ,
ctime: "{self.ctime}" ,
bin_value: "{self.__bin_value}" ,
)
'''


class ModbusIO(object):
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(self):
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True
        self.__id = None
        self.__isConnected = False
        self.__context_action_error: str = 'exit'
        self.__isInContext = False
        self.__client = ModbusSerialClient(
            port=ModbusParams.PORT,
            baudrate=ModbusParams.BAUDRATE,
            parity=ModbusParams.PARITY,
            stopbits=ModbusParams.STOPBITS,
            bytesize=ModbusParams.BYTESIZE,
            timeout=ModbusParams.TIMEOUT,
            retries=ModbusParams.RETRIES,
            name=self.__class__.__name__,
        )
        self.__thread_lock = threading.Lock()

    def __enter__(self):
        self.__thread_lock.acquire_lock()
        try:
            self.__client.connect()
            self.__isConnected = True
        except Exception as e:
            self.__context_action_error = 'enter'
            self.__exit__(e.__class__, e, e.__traceback__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _log.exception(f'ModbusIO {self.__context_action_error} with error: {exc_val}')
        if self.__client and self.__client.is_socket_open():
            self.__client.close()
        self.__isConnected = False
        self.__thread_lock.release_lock()
        return True

    def read(self, address: int) -> ModbusDataStruct:
        if not self.__isConnected:
            _log.warning('ModbusIO read warning: not connected, it must be called from context manager')
            return ModbusDataStruct({})
        if self.__id is None:
            _log.warning('ModbusIO read warning: id is None')
            return ModbusDataStruct({})
        result_data = {}
        try:
            result_data: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
        except AttributeError as e:
            _log.warning(f'ModbusIO read warning: {e}\naddress: {address}')
        except Exception as e:
            _log.warning(f'ModbusIO read ModbusPDU error: {traceback.format_exc()}\naddress: {address}')
        finally:
            return ModbusDataStruct(result_data)

    def write(self, address: int, value: int) -> None | bool:
        if not self.__isConnected:
            _log.warning('ModbusIO read warning: not connected, it must be called from context manager')
            return False
        if self.__id is None:
            _log.warning('ModbusIO read warning: id is None')
            return False
        try:
            result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
            _log.info(f'ModbusIO write: address: {address}\nvalue: {value}\nresult: {result}\nfc: {result.function_code}')
            if result and result.isError():
                _log.exception(f'ModbusIO write error.\naddress: {address}\nvalue: {value}')
                return False
            return True
        except Exception as e:
            _log.exception(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')
            return False

    def set_id(self, id: int) -> typing.Self:
        if not isinstance(id, int) or id < 0:
            raise TypeError('Id of ModbusIO must be int and greater than 0')
        if self.__id == id:
            return
        self.__id: int = id
        return self
