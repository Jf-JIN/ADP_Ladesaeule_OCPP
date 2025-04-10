
from pymodbus.pdu.pdu import *
from pymodbus.client import *
from const.Const_Logger import *
from const.ConstModbus import *

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

    def __load_ModbusDataUnit(self, ModbusDataUnit: ModbusPDU):
        self.__ModbusDataUnit = ModbusDataUnit
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
        }


class ModbusHandler(object):
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

    def connect(self) -> ModbusSerialClient:
        if self.__id is None:
            _log.warning('Modbus Id is not set, please set Modbus Id first')
            self.__isConnected = False
            return None
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
        self.__isConnected = True
        return self.__client

    def set_id(self, id: int) -> None:
        if not isinstance(id, int) or id < 0:
            raise TypeError('Id of ModbusIO must be int and greater than 0')
        if self.__id == id:
            return
        self.__id: int = id
        if not self.__isConnected:
            self.connect()

    def read(self, address: int) -> None | ModbusDataStruct:
        """
        从指定的Modbus寄存器地址读取数据.

        - 参数:
            - address(int): 要读取的Modbus寄存器地址.

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.

        - 异常:
            - 当读取过程中发生任何异常时, 会被捕获并返回 None.
        """
        try:
            result: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
            return ModbusDataStruct(result)
        except Exception as e:
            _log.exception(f'ModbusIO read error: {e}\naddress: {address}')
            return None

    def write(self, address: int, value: int | list) -> None | ModbusDataStruct:
        if isinstance(value, int):
            value = [value]
        try:
            result: ModbusPDU = self.__client.write_registers(address=address, values=value, slave=self.__id)
            return ModbusDataStruct(result)
        except Exception as e:
            _log.exception(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')
            return None

        # def write(self, address: int, value: int, bit_operation: int | None = None) -> None | bool:
        #     """
        #     写入寄存器

        #     - 参数:
        #         - address(int): 要写入的Modbus寄存器地址.
        #         - value(int): 要写入的整数值.
        #         - bit_operation(int|None): 按位操作, 可选参数, 默认为None.
        #             - 如果为None, 则直接写入整数值.
        #             - 如果为0, 则按位置零
        #             - 如果为1或其他值, 则按位置一

        #     - 返回值:
        #         - 如果写入成功, 返回True.
        #         - 如果写入失败或发生错误, 返回False.

        #     - 异常:
        #         - 当写入过程中发生任何异常时, 会被捕获并返回 False.
        #     """
        #     if bit_operation is not None:  # 按位操作
        #         ori_value = self.read(address=address)
        #         if ori_value is None:
        #             _log.error(f'ModbusIO read error by writing.\naddress: {address}')
        #             return False
        #         if bit_operation == 0:  # 置0
        #             ori_value &= ~value
        #             value = ori_value
        #         else:  # 置1
        #             ori_value |= value
        #             value = ori_value
        #     try:
        #         result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
        #         _log.debug(result, result.registers[0])
        #         if result.isError():
        #             _log.exception(f'ModbusIO write error.\naddress: {address}\nvalue: {value}')
        #             return False
        #         return True
        #     except Exception as e:
        #         _log.exception(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')
        #         return False
