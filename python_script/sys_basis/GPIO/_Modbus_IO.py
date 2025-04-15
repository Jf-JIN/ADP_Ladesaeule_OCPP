
# from pymodbus.pdu.pdu import ModbusPDU  # 实际使用
# from pymodbus.client import ModbusSerialClient  # 实际使用

from ._test_Module import ModbusPDU, ModbusSerialClient  # 用于测试

from const.Const_Parameter import *
from const.GPIO_Parameter import BitsFlag, EVSEErrorInfo, EVSERegAddress, ModbusParams
import threading

_log = Log.MODBUS


class ModbusIO(object):
    isSelfChecking: set = set()
    __instance__: 'ModbusIO' = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(self, id: int) -> None:
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True
        if not isinstance(id, int):
            raise TypeError('Id of ModbusIO must be int')
        self.__id: int = id
        self.__context_action_error: str = 'exit'
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
        if self.__id in self.__class__.isSelfChecking:
            self.__exit__(None, None, None)
        self.__thread_lock.acquire_lock()
        try:
            self.__client.connect()
        except Exception as e:
            self.__context_action_error = 'enter'
            self.__exit__(e.__class__, e, e.__traceback__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _log.exception(f'ModbusIO {self.__context_action_error} with error: {exc_val}')
        if self.__client and self.__client.is_socket_open():
            self.__client.close()
        self.__thread_lock.release_lock()
        return True

    def is_socket_valid(self) -> bool:
        try:
            # 只要访问 in_waiting 就会触发底层检查
            _ = self.__client.socket.in_waiting
            return True
        except Exception as e:
            _log.warning(f"Modbus socket invalid: {e}")
            return False

    def read_PDU(self, address: int) -> None | ModbusPDU:
        result_data = None
        # with self.__thread_lock:
        try:
            result_data: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
        except AttributeError as e:
            _log.warning(f'ModbusIO read warning: {e}\naddress: {address}')
        except Exception as e:
            _log.warning(f'ModbusIO read ModbusPDU error: {traceback.format_exc()}\naddress: {address}')
        finally:
            return result_data

    def read(self, address: int) -> None | int:
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
        result_data = None
        # _log.info(f'threadlock {self.__thread_lock.locked()}')
        # with self.__thread_lock:
        try:
            result: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
            # result: ModbusPDU = self.__client.read_input_registers(address=address, slave=self.__id)
            # _log.critical(f'function_code: {result.function_code}\naddress: {address}\ndata: result.registers[0]\nresult: {result.registers}')
            # _log.info(f'function_code: {result.function_code}\naddress: {address}\nresult: {result}')
            if result and not result.isError():
                result_data: int = result.registers[0]
                # _log.info(f'function_code: {result.function_code}\naddress: {address}\nresult: {result}')
            else:
                _log.error(f'ModbusIO read error.\naddress: {address}')
                # _log.info(f'function_code: {result.function_code}\naddress: {address}\nresult: {result}\nexception_code: {result.exception_code}')
        except Exception as e:
            _log.exception(f'ModbusIO read error: {e}\naddress: {address}')
        finally:
            return result_data

    def write(self, address: int, value: int, bit_operation: int | None = None) -> None | bool:
        """
        写入寄存器

        - 参数:
            - address(int): 要写入的Modbus寄存器地址.
            - value(int): 要写入的整数值.
            - bit_operation(int|None): 按位操作, 可选参数, 默认为None.
                - 如果为None, 则直接写入整数值.
                - 如果为0, 则按位置零
                - 如果为1或其他值, 则按位置一

        - 返回值:
            - 如果写入成功, 返回True.
            - 如果写入失败或发生错误, 返回False.

        - 异常:
            - 当写入过程中发生任何异常时, 会被捕获并返回 False.
        """
        if bit_operation is not None:  # 按位操作
            ori_value = self.read(address=address)
            if ori_value is None:
                _log.error(f'ModbusIO read error by writing.\naddress: {address}')
                return False
            if bit_operation == 0:  # 置0
                ori_value &= ~value
                value = ori_value
            else:  # 置1
                ori_value |= value
                value = ori_value

        # with self.__thread_lock:
        try:
            # _log.info(f'threadlock {self.__thread_lock.locked()}')
            result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
            _log.info(f'[WRITE] function_code: {result.function_code}\naddress: {address}\nresult: {result}')
            # check_res = self.__client.read_holding_registers(address=address, slave=self.__id)
            # _log.info(f'[CHECK] function_code: {check_res.function_code}\naddress: {address}\nresult: {check_res}')
            # _log.debug(result, result.registers[0])
            if result and result.isError():
                _log.exception(f'ModbusIO write error.\naddress: {address}\nvalue: {value}')
                return False
            # _log.info(f'threadlock end {self.__thread_lock.locked()}')
            return True
        except Exception as e:
            _log.exception(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')
            return False

    def read_evse_status_fails(self) -> None | set:
        """
        读取EVSE状态和故障

        - 返回值: 
            - None: 读取失败
            - set: EVSE状态和故障集合
        """
        data_list = set()
        data_list.add(EVSEErrorInfo.RELAY_ON)
        return data_list
        # status: None | int = self.read(address=EVSERegAddress.EVSE_STATUS_FAILS)
        # if status is None:
        #     return None
        # if status & BitsFlag.REG1007.RELAY_OFF:
        #     data_list.add(EVSEErrorInfo.RELAY_OFF)
        # else:
        #     data_list.add(EVSEErrorInfo.RELAY_ON)
        # if status & BitsFlag.REG1007.DIODE_CHECK_FAIL:
        #     data_list.add(EVSEErrorInfo.DIODE_CHECK_FAIL)
        # if status & BitsFlag.REG1007.VENT_REQUIRED_FAIL:
        #     data_list.add(EVSEErrorInfo.VENT_REQUIRED_FAIL)
        # if status & BitsFlag.REG1007.WAITING_FOR_PILOT_RELEASE:
        #     data_list.add(EVSEErrorInfo.WAITING_FOR_PILOT_RELEASE)
        # if status & BitsFlag.REG1007.RCD_CHECK_ERROR:
        #     data_list.add(EVSEErrorInfo.RCD_CHECK_ERROR)
        # return data_list

    def read_vehicle_status(self) -> None | int:
        """
        读取车辆状态

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        return 2
        # return self.read(address=EVSERegAddress.VEHICLE_STATE)

    def read_current_min(self) -> None | int:
        """
        读取允许的最小电流值

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        return self.read(address=EVSERegAddress.CURRENT_MIN)

    def read_current_max(self) -> None | int:
        """
        读取允许的最大电流值

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        return self.read(address=EVSERegAddress.CURRENT_MAX)

    def run_selftest_and_RCD_test_procedure(self) -> None | bool:
        """
        执行自检和RCD测试程序

        注意: 在EVSE类中, 必须在自检结束时调用`finish_selftest_and_RCD_test_procedure`来关闭自检和RCD测试程序, 否则对应id下的Modbus无法进行读取
        """
        self.__class__.isSelfChecking.add(self.__id)
        return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.SELFTEST_RCDTEST)

    def finish_selftest_and_RCD_test_procedure(self) -> None:
        """
        结束自检和RCD测试程序
        """
        self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.SELFTEST_RCDTEST, bit_operation=0)

    def finish_selftest_and_RCD_test_procedure_with_RCD(self) -> None:
        """
        结束自检和RCD测试程序
        """
        self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.SELFTEST_RCDTEST, bit_operation=0)
        self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.CLEAR_RCD_ERROR, bit_operation=0)

    def set_current(self, value: int) -> None | bool:
        return self.write(address=EVSERegAddress.CONFIGURED_AMPS, value=value)

    def enable_charge(self, flag: bool = True) -> None | bool:
        """
        允许充电/停止充电

        - 返回值:
            - 如果写入成功, 返回True.
            - 如果写入失败或发生错误, 返回False.
        """
        if flag:
            return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW, bit_operation=0)
        else:
            return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW, bit_operation=1)

    def enable_RCD(self, flag: bool) -> None | bool:
        """ 
        开启/关闭RCD检查
        """
        if flag:
            return self.write(address=EVSERegAddress.CHARGE_OPERATION, value=BitsFlag.REG2005.ENABLE_RCD_FEEDBACK, bit_operation=1)
        else:
            return self.write(address=EVSERegAddress.CHARGE_OPERATION, value=BitsFlag.REG2005.ENABLE_RCD_FEEDBACK, bit_operation=0)

    def clear_RCD(self) -> None | bool:
        """ 
        清除RCD错误
        """
        return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.CLEAR_RCD_ERROR, bit_operation=0)
