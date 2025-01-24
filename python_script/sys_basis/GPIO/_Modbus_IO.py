
from pymodbus.pdu.pdu import ModbusPDU
from pymodbus.client import ModbusSerialClient
from const.Const_Parameter import *
from const.GPIO_Parameter import BitsFlag, EVSERegAddress, ModbusParams

_debug = Log.MODBUS.debug
_error = Log.MODBUS.error
_exception = Log.MODBUS.exception


class ModbusIO(object):
    isSelfChecking: set = set()

    def __init__(self, id: int):
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

    def __enter__(self):
        if self.__id in self.isSelfChecking:
            self.__exit__(None, None, None)
        try:
            self.__client.connect()
        except Exception as e:
            self.__context_action_error = 'enter'
            self.__exit__(e.__class__, e, e.__traceback__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            _exception(f'ModbusIO {self.__context_action_error} with error: {exc_val}')
        return True

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
            if not result.isError():
                result_data: int = result.registers[0]
            else:
                _error(f'ModbusIO read error.\naddress: {address}')
        except Exception as e:
            _exception(f'ModbusIO read error: {e}\naddress: {address}')
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
                _error(f'ModbusIO read error by writing.\naddress: {address}')
                return False
            if bit_operation == 0:  # 置0
                ori_value &= ~(value)
                value = ori_value
            else:  # 置1
                ori_value |= value
                value = ori_value
        try:
            result: ModbusPDU = self.__client.write_registers(address=address, values=[value], slave=self.__id)
            _debug(result, result.registers[0])
            if result.isError():
                _exception(f'ModbusIO write error.\naddress: {address}\nvalue: {value}')
                return False
            return True
        except Exception as e:
            _exception(f'ModbusIO write error: {e}\naddress: {address}\nvalue: {value}')

    def read_evse_status_and_fails(self) -> None | set:
        """ 
        读取EVSE状态和故障

        - 返回值：
            - None: 读取失败
            - set: EVSE状态和故障集合
        """
        data_list = set()
        status: None | int = self.read(address=EVSERegAddress.EVSE_STATUS_FAILS)
        if status is None:
            return None
        if status & BitsFlag.REG1007.RELAY_OFF:
            data_list.add('Relay Off')
        else:
            data_list.add('Relay On')
        if status & BitsFlag.REG1007.DIODE_CHECK_FAIL:
            data_list.add('diode Check Fail')
        if status & BitsFlag.REG1007.VENT_REQUIRED_FAIL:
            data_list.add('Vent Required Fail')
        if status & BitsFlag.REG1007.WAITING_FOR_PILOT_RELEASE:
            data_list.add('Waiting For Pilot Release')
        if status & BitsFlag.REG1007.RCD_CHECK_ERROR:
            data_list.add('RCD Check Error')
        return data_list

    def read_vehicle_status(self) -> None | bool:
        """ 
        读取车辆状态

        - 返回值:
            - 如果读取成功, 返回寄存器中的整数值.
            - 如果读取失败或发生错误, 返回None.
        """
        return self.read(address=EVSERegAddress.VEHICLE_STATE)

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

    def disable_charge(self) -> None | bool:
        """ 
        立即停止充电

        - 返回值:
            - 如果写入成功, 返回True.
            - 如果写入失败或发生错误, 返回False.
        """
        return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW)

    def enable_charge(self) -> None | bool:
        """ 
        允许开始充电

        - 返回值:
            - 如果写入成功, 返回True.
            - 如果写入失败或发生错误, 返回False.
        """
        return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.TURN_OFF_CHARGING_NOW, bit_operation=0)

    def run_selftest_and_RCD_test_procedure(self) -> None | bool:
        """
        注意: 在EVSE类中, 需要在自检结束时将 id 从 isSelfChecking中删除, 否则无法继续读取数据.
        """
        __class__.isSelfChecking.add(self.__id)
        return self.write(address=EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value=BitsFlag.REG1004.SELFTEST_RCDTEST)

    def enableRCD(self) -> None | bool:
        return self.write(address=EVSERegAddress.CHARGE_OPERATION, value=BitsFlag.REG2005.ENABLE_RCD_FEEDBACK)
