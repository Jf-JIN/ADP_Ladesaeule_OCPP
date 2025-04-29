

from ._import_modbus_gpio import *

from const.Const_Parameter import *
from const.GPIO_Parameter import BitsFlag, EVSEErrorInfo, EVSERegAddress, GPIOParams, ModbusParams, REG1006
import threading
import traceback

from DToolslib import Inner_Decorators

_log = Log.MODBUS


class CallerStruct:
    def __init__(self, data: dict):
        self.caller = data.get('caller', '')
        self.caller_name = data.get('caller_name', '')
        self.class_name = data.get('class_name', '')
        self.line_num = data.get('line_num', '')
        self.module_name = data.get('module_name', '')
        self.script_name = data.get('script_name', '')
        self.script_path = data.get('script_path', '')
        self.thread_name = data.get('thread_name', '')


class ModbusIO(object):
    isSelfChecking: set = set()
    __instance__: 'ModbusIO' = None
    __lock__: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            with cls.__lock__:
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
        # _log.info(f'Enter {self.__class__.__name__} {self.__id} lock')  # {self.__thread_lock.locked()}')
        self.__thread_lock.acquire()
        # _log.info('已申请锁')
        try:
            # _log.info('尝试连接')
            self.__client.connect()
        except Exception as e:
            # _log.exception(f'ModbusIO {self.__id} 连接失败')
            self.__context_action_error = 'enter'
            self.__exit__(e.__class__, e, e.__traceback__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _log.exception(f'ModbusIO {self.__context_action_error} with error: {exc_val}')
        if self.__client and self.__client.is_socket_open():
            self.__client.close()
        self.__thread_lock.release()
        # _log.info(f'Exit {self.__class__.__name__} {self.__id} lock')  # {self.__thread_lock.locked()}')
        return True

    # @Inner_Decorators.time_counter
    # def read_PDU(self, address: int) -> None | ModbusPDU:
    #     result_data = None
    #     try:
    #         result_data: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
    #     except AttributeError as e:
    #         _log.warning(f'ModbusIO read warning: {e}\naddress: {address}')
    #     except Exception as e:
    #         _log.warning(f'ModbusIO read ModbusPDU error: {traceback.format_exc()}\naddress: {address}')
    #     finally:
    #         return result_data

    # @Inner_Decorators.time_counter
    def read_PDU(self, address: int, count: int) -> None | ModbusPDU:
        result_data = None
        try:
            result_data: ModbusPDU = self.__client.read_holding_registers(address=address, count=count, slave=self.__id)
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
        try:
            result: ModbusPDU = self.__client.read_holding_registers(address=address, slave=self.__id)
            if result and not result.isError():
                result_data: int = result.registers[0]
                # _log.info(f'function_code: {result.function_code}\naddress: {address}\nresult: {result}')
            else:
                _log.warning(f'ModbusIO read error.\naddress: {address}')
                # _log.info(f'function_code: {result.function_code}\naddress: {address}\nresult: {result}\nexception_code: {result.exception_code}')
        except Exception as e:
            _log.warning(f'ModbusIO read error: {traceback.format_exc()}\naddress: {address}')
        finally:
            return result_data

    def write(self, address: int, value: int, bit_operation: int | None = None) -> bool:
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
        try:
            result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
            # _log.info(f'[WRITE] function_code: {result.function_code}\naddress: {address}\nresult: {result}')
            # check_res = self.__client.read_holding_registers(address=address, slave=self.__id)
            # _log.info(f'[CHECK] function_code: {check_res.function_code}\naddress: {address}\nresult: {check_res}')
            if result and result.isError():
                _log.warning(f'ModbusIO write error.\naddress: {address}\nvalue: {value}')
                return False
            self.__check_write(address=address, value=value)
            return True
        except Exception as e:
            _log.warning(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')
            return False

    def __check_write(self, address: int, value: int) -> bool:
        retry_count = GPIOParams.EVSE_WRITE_RETRY
        while retry_count > 0:
            check_res = self.__client.read_holding_registers(address=address, slave=self.__id)
            if check_res and check_res.isError():
                _log.warning(f'ModbusIO write_check error.\naddress: {address}\nvalue: {value}')
                retry_count -= 1
                continue
            if check_res.registers[0] == value:
                return True
            else:
                _log.info(f'retry write {GPIOParams.EVSE_WRITE_RETRY-retry_count} times')
                result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
                if result.isError():
                    _log.warning(f'ModbusIO rewrite error.\naddress: {address}\nvalue: {value}')
            retry_count -= 1

    def read_evse_status_fails(self) -> None | set:
        """
        读取EVSE状态和故障

        - 返回值: 
            - None: 读取失败
            - set: EVSE状态和故障集合
        """
        return {EVSEErrorInfo.RELAY_ON}
        # data_list = set()
        # data_list.add(EVSEErrorInfo.RELAY_ON)
        # return data_list
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
        # return 2
        return self.read(address=EVSERegAddress.VEHICLE_STATE)

    def read_current_min(self) -> None | int:
        """
        读取允许的最小电流值

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        # _log.info("read_current_min")
        return self.read(address=EVSERegAddress.CURRENT_MIN)

    def read_current_max(self) -> None | int:
        """
        读取允许的最大电流值

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        _log.info("read_current_max")
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

    def set_current(self, value: int) -> bool:
        return self.write(address=EVSERegAddress.CONFIGURED_AMPS, value=value)

    def enable_charge(self, flag: bool = True) -> bool:
        """
        允许充电/停止充电

        - 返回值:
            - 如果写入成功, 返回True.
            - 如果写入失败或发生错误, 返回False.
        """
        if flag:
            current_min = self.read_current_min()
            if current_min is None:
                current_min = 5
            res_1000 = self.write(address=EVSERegAddress.CONFIGURED_AMPS, value=current_min)
            if not res_1000:
                return False
            res_1004: bool = self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW, bit_operation=0)
            _log.info(f"res_1004 write: {res_1004}")
            if not res_1004:
                _log.warning(f"res_1004 write failed: {res_1004}")
                # return False
            if self.read(address=EVSERegAddress.EVSE_STATE) == REG1006.STEADY:
                return True
            res_1006: bool = self.write(address=EVSERegAddress.EVSE_STATE, value=REG1006.STEADY)
            _log.info(f"res_1006 write: {res_1006}")
            return res_1006
        else:
            res_1004 = self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW, bit_operation=1)
            # _log.info(f"res_1004 write: {res_1004}")
            if not res_1004:
                _log.warning(f"res_1004 write failed: {res_1004}")
                # return False
            res_1006: bool = self.write(address=EVSERegAddress.EVSE_STATE, value=REG1006.OFF)
            # _log.info(f"res_1006 write: {res_1006}")
            return res_1006

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

    def set_default_current(self, value: int) -> None | bool:
        """ 
        设置默认电流
        """
        return self.write(address=EVSERegAddress.DEFAULT_AMPS, value=value)
