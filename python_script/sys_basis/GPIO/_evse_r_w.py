
from typing import Optional, List
import traceback
from const.GPIO_Parameter import *
from pymodbus import ModbusException
from sys_basis.XSignal import XSignal

class EVSEReadWrite(object):

    def __init__(self, client):
        """
        Modbus读写功能
        读写的结果被打包成一个新列表，结构为[flag, registers_result_list, message]
        flag用于标记此命令是否成功执行
        参数:
             - client: Modbus客户端对象
        """

        self._client = client
        self.__signal_EVSE_info = XSignal()
        self.__signal_EVSE_read_data = XSignal()
        self.__signal_EVSE_failure = XSignal()
        self.__signal_EVSE_check_connection = XSignal()
        self.__vehicle_state = [0, 'ready', 'EV is present', 'charging', 'charging with ventilation',
                                'failure (e.g. diode check, RCD failure)']  # get_vehicle_state返回1~5，0用于占位
        self.__EVSE_state = [0, 'steady 12V', 'PWM is being generated(only if 1000 >= 6)', 'OFF, steady 12V']

    # @property
    # def signal_EVSE_read_data(self):
    #     return self.__signal_EVSE_read_data
    #
    # @property
    # def signal_EVSE_failure(self):
    #     return self.__signal_EVSE_failure

    def get_allowed_current(self) -> Optional[List[int]]:
        """
         6 / 13 / 20 / 32 / 63 / 80 A
         Maximum current limitation according to a cable based on PP
         resistor detection
        返回:
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        #allowed_current = self.read_register(address=1003)
        #self.signal_EVSE_read_data.emit(allowed_current)
        return self.read_register(method= 'get_allowed_current', address=1003)

    def get_actual_current(self) -> Optional[List[int]]:
        """
         Actual amps value output
        返回:
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        return self.read_register(method= 'get_actual_current', address=1001)
        #return [ResultFlag.SUCCESS,[20],'测试数据']#测试

    def get_vehicle_state(self) -> Optional[List[int]]:
        """
        Vehicle state:
            1: ready
            2: EV is present
            3: charging
            4: charging with ventilation
            5: failure (e.g. diode check, RCD failure)
        返回:
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        return self.read_register(method='get_vehicle_state', address=1002)

    def get_EVSE_state(self) -> Optional[List[int]]:
        """
        EVSE state
            1: steady 12V
            2: PWM is being generated(only if 1000 >= 6)
            3: OFF, steady 12V
        返回:
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        #self.__send_signal_info(self.__EVSE_state[self.read_register(address=1006)[0]])
        return self.read_register(method= 'get_EVSE_state', address=1006)

    def get_EVSE_status_fails(self):
        """
         EVSE status and fails:
             bit0: relay on/off (暂定0 = on, 1 = off)
             bit1: diode check fail
             bit2: vent required fail
             bit3: waiting for pilot release (error recovery delay)
             bit4: RCD check error
             bit5:
             bit6-bit15: reserved
        """

        return self.read_register(method= 'get_EVSE_status_fails', address = 1007)

    def get_EVSE_config(self) -> Optional[List[int]]:
        return self.read_register(method= 'get_EVSE_config', address = 2005)

    def get_min_current(self) -> Optional[List[int]]:
        return self.read_register(method= 'get_min_current', address = 2002)

    def read_register(self, method: str, address: int, count: int = 1, slave: int = 1) -> Optional[List[int]]:
        """
        读取保持寄存器（Holding Registers）
        参数:
            - method: 使用写功能的方法名
            - address: 起始寄存器地址（零偏移）
            - count: 读取的寄存器数量，默认为 1
            - slave: 从站地址，EVSE 从站地址为 1
        返回
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        try:
            # 读取寄存器
            result = self._client.read_holding_registers(address=address, count=count, slave=slave)
            if not result.isError():
                message = [ResultFlag.SUCCESS, result.registers, f"=={method}==\n读取成功\n成功读取到 {count} 个寄存器，从地址 {address} 开始: {result.registers}"]
            else:
                message = [ResultFlag.FAIL, result.registers, f"=={method}==\n==读取失败==\n功能码返回错误或无效响应: {result.registers}"]

        except ModbusException:
            message = [ResultFlag.FAIL, None, f"=={method}==\n==读取错误==\n发送或接收数据时发生 Modbus 错误: {traceback.format_exc()}"]

        except Exception:
            message = [ResultFlag.FAIL, None, f"=={method}==\n==读取错误==\n发送或接收数据时发生未知错误: {traceback.format_exc()}"]

        return message

    def turn_off_charging_now(self):
        return self.write_register(method= '__turn_off_charging_now', address=1004, value=REG1004.TURN_OFF_CHARGING_NOW)

    def run_selftest_and_RCD_test_procedure(self):
        return self.write_register(method= 'run_selftest_and_RCD_test_procedure', address=1004 ,value=REG1004.RUN_SELFTEST_AND_RCD_TEST_PROCEDURE)

    def enableRCD(self):
        return self.write_register(method= 'enableRCD', address=2005, value=REG2005.RCD_FEEDBACK_ENABLE)


    def write_register(self, method: str, address: int, value: int, slave: int = 1,) -> Optional[List[int]]:
        """
        写入一个保持寄存器（Holding Register）
        参数:
            - method: 使用写功能的方法名
            - address: 寄存器地址
            - value: 要写入的值
            - slave: 从站地址，默认值为 1
        返回:
            - 成功时返回[成功flag,[寄存器返回值列表]，'消息']，失败时返回 [失败flag,None(pymodbus要求返回None),'消息']
        """
        try:
            # 将值封装成列表，因为 pymodbus 的 write_registers 接收列表
            result = self._client.write_registers(address=address, values=[value], slave=slave)
            if not result.isError():
                message = [ResultFlag.SUCCESS, result.registers,f"=={method}==\n写入成功\n成功写入寄存器 {address}，值为 {value}"]
            else:
                message = [ResultFlag.FAIL, None,f"=={method}==\n==写入失败==\n写入寄存器 {address}，值为 {value}"]

        except ModbusException as e:
               # 捕获 Modbus 异常
               message = [ResultFlag.FAIL, None, f"=={method}==\n==写入错误==\n发送或接收数据时发生 Modbus 错误: {traceback.format_exc()}"]
        except Exception as e:
               # 捕获其他非 Modbus 异常
               message = [ResultFlag.FAIL, None, f"=={method}==\n==写入错误==\n发送或接收数据时发生未知错误: {traceback.format_exc()}"]
        return message


    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_EVSE_info, error_hint='send_signal_info', log=None,
                           doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False,
                      doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
            - signal(XSignal): 信号对象
            - error_hint(str): 错误提示
            - log: 日志器动作
            - doShowTitle(bool): 是否显示标题
            - doPrintInfo(bool): 是否打印信息
            - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            if doShowTitle:
                temp = f'< EVSECommunication >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if doShowTitle:
                error_text = f'< EVSECommunication >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(temp)

