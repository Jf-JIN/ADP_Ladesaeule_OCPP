import time
from typing import Optional, List
from _Decorator_check_flag import check_flag
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from pymodbus.client import ModbusSerialClient
from sys_basis.XSignal import XSignal
from sys_basis.GPIO._evse_r_w import EVSEReadWrite
#from sys_basis.GPIO._evse_r_w_test import EVSEReadWrite
from _Thread_evse_output_current import ThreadOutputCurrent
from _Thread_evse_fail_check import ThreadFailCheck
from _Thread_evse_vehicle_state import ThreadVehicleState
from _Thread_evse_try_connect import ThreadTryConnection


class EVSEManager(object):



    def __init__(self, RCD: bool, port=GPIOParams.PORT, baudrate=GPIOParams.BAUDRATE, poll_interval=GPIOParams.POLL_INTERVAL, poll_interval_check= GPIOParams.POLL_INTERVAL_CHECK,
                 parity=GPIOParams.PARITY, stopbits=GPIOParams.STOPBITS, bytesize=GPIOParams.BYTESIZE, timeout=GPIOParams.TIMEOUT,):
        """
        初始化通信对象，设置串口参数
        参数:
             - port: 串口端口，默认 '/dev/ttyS0'
             - baudrate: 波特率，默认 9600
             - poll_interval: 读取数据的间隔时间，默认 5 秒
             - poll_interval_check: 检查充电头是否拔出，默认 1 秒
             - parity: 有无校验位
             - stopbits: 停止位
             - bytesize: 数据位
             - timeout: 超时时间
             - RCD: 是否使用RCD
        """

        self.__port = port
        self.__baudrate = baudrate               
        self.__poll_interval= poll_interval
        self.__poll_interval_check= poll_interval_check
        self.__parity = parity
        self.__stopbits = stopbits
        self.__bytesize = bytesize
        self.__timeout = timeout

        self.__output_current_polling_thread = None
        self.__vehicle_state_polling_thread = None
        self.__evse_failure_polling_thread = None
        self.__checking_connection_thread = None
        self.__isConnected = False
        self.__isRCD = RCD
        self.__Fail = None
        self.__limitCurrent = None
        self.__min_current = None

        self._client = ModbusSerialClient(
            port=self.__port,        # 串口设备
            baudrate=self.__baudrate,  # 波特率
            parity=self.__parity,             # 无校验位
            stopbits=self.__stopbits,             # 停止位
            bytesize=self.__bytesize,             # 数据位
            timeout=self.__timeout               # 超时时间
        )

        self.__signal_EVSE_info = XSignal()
        self.__signal_EVSE_min_current = XSignal()
        self.__signal_EVSE_actual_current = XSignal()
        self.__signal_EVSE_failure = XSignal()
        self.__signal_vehicle_state = XSignal()
        self.__vehicle_state_list = [0, 'ready', 'EV is present', 'charging', 'charging with ventilation','failure (e.g. diode check, RCD failure)']  # get_vehicle_state返回1~5，0用于占位
        self.__vehicle_state = None
        self.__EVSE_state_list = [0,'steady 12V','PWM is being generated(only if 1000 >= 6)','OFF, steady 12V']
        self.EVSE = EVSEReadWrite(client= self._client)
        self.booting()

    @property
    def signal_EVSE_min_current(self):
        return self.__signal_EVSE_min_current

    @property
    def signal_EVSE_actual_current(self):
        return self.__signal_EVSE_actual_current

    @property
    def signal_EVSE_failure(self):
        return self.__signal_EVSE_failure

    @property
    def signal_vehicle_state(self):
        return self.__signal_vehicle_state


    def booting(self):
        if self.isConnected():
            allowed_current = self.get_allowed_current()
            min_current= self.get_min_current()
            if allowed_current:
                self._send_signal_info(f"允许最大电流为{allowed_current}A")
                self.__limitCurrent = allowed_current  # 获取允许的电流值
            else:
                self._send_signal_info("获取允许电流失败")
                self.__limitCurrent = 0  # 设置默认值或其他处理方式

            if min_current:
                self._send_signal_info(f"允许最小电流为{min_current}A")
            else:
                self._send_signal_info("获取最小电流失败")

            if self.__isRCD:
                self.enable_RCD()

            self.__clear(address=1004,bit=REG1004.TURN_OFF_CHARGING_NOW)

            self.selftest()
            if not self.__Fail:
                self.start_polling()
        else:
            self.__limitCurrent = 0  # 如果连接失败，设置默认值
            self._send_signal_info("EVSE启动失败")
            self.signal_EVSE_failure.emit(True)

        #print('booting end')


    def selftest(self):
        # 运行自检和 RCD 检测程序
        self.EVSE.run_selftest_and_RCD_test_procedure()
        time.sleep(31)

        if self.__isRCD:
            # 检查 EVSE 状态
            flag, value, message = self.EVSE.get_EVSE_status_fails()
            # 如果失败标志为 FAIL，检查连接
            if flag == ResultFlag.FAIL:
                self.checking_connection()
            # 如果包含 RCD_CHECK_ERROR，清除错误
            elif value & EVSEFails.RCD_CHECK_ERROR:
                self.__clear(address=1007, bit=EVSEFails.RCD_CHECK_ERROR)
            else:
                self.__Fail = True
                self._send_signal_info("RCD failed to alarm")
                self.signal_EVSE_failure.emit(True)

    def isConnected(self) -> bool:
        """
        是否连接到设备
        返回:
            - 成功时返回 True，失败时返回 False
        """
        if self._client.connect():
            self._send_signal_info(f"连接成功: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__isConnected = True
            return True
        else:
            self._send_signal_info(f"连接失败: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__isConnected = False
            self.checking_connection()
            return False

    @check_flag(used_method =lambda self: self.EVSE.get_EVSE_config())
    def isRCD(self, value, message) -> bool:
        if value:
            if value & REG2005.RCD_FEEDBACK_ENABLE:
                self.__isRCD = True
            else:
                self.__isRCD = False
        self._send_signal_info(message)
        return self.__isRCD

    @check_flag(used_method =lambda self: self.EVSE.enableRCD())
    def enable_RCD(self,value,message):
        self._send_signal_info(message)

    @check_flag(used_method=lambda self: self.EVSE.turn_off_charging_now())
    def __turn_off_charging_now(self,value, message):
        self._send_signal_info(message)

    @check_flag(used_method =lambda self: self.EVSE.get_allowed_current())
    def get_allowed_current(self,value,message) -> int:
        if value:
            allowed_current = value[0]
        else:
            allowed_current = None
        self._send_signal_info(message)
        return allowed_current

    @check_flag(used_method =lambda self: self.EVSE.get_vehicle_state())
    def get_vehicle_state(self,value,message) -> int:
        """
        检查flag,获取并改变车辆状态,并赋值给self.__vehicle_state
        返回:
            - 成功时返回 self.__vehicle_state，失败时返回 None
        """
        if value:
            self.__vehicle_state = value[0]
            self.signal_vehicle_state.emit(f'{self.__vehicle_state_list[self.__vehicle_state]}')
        else:
            self.__vehicle_state = None
        self._send_signal_info(message)
        return self.__vehicle_state

    @check_flag(used_method =lambda self: self.EVSE.get_min_current())
    def get_min_current(self,value,message) -> int:
        """
              检查flag,获取最低电流并发送
              返回:
                  - 成功时返回 self.__min_current，失败时返回 None
              """
        if value:
            self.__min_current = value[0]
            self.signal_EVSE_min_current.emit(self.__min_current)
        else:
            self.__min_current = None
        self._send_signal_info(message)

        return self.__min_current

    def send_actual_current(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.__handle_connection_error(message)
        else:
            actual_current = value[0]
            self.signal_EVSE_actual_current.emit(actual_current)
            #print(f'测试{actual_current}A')

    def handle_vehicle_state(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.__handle_connection_error(message)
        else:
            self.__vehicle_state = value[0]
            if self.__vehicle_state == VehicleState.FAILURE:
                self.__emergency_shut_down()
                self._send_signal_info(f'车辆状态异常，已紧急断电')
            self.signal_vehicle_state.emit(f'{self.__vehicle_state_list[self.__vehicle_state]}')

    def handle_EVSE_fail(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.__handle_connection_error(message)
        else:
            state_value = value[0]  # 假设 value 是列表，我们取第一个元素
            num_bits = EVSEFails.NUM_BIT  # 你可以根据实际情况调整位数
            status = [False] * num_bits  # 初始化为全 False

            # 按位检查 state_value 的每一位
            for bit_position in range(num_bits):
                status[bit_position] = bool(state_value & (1 << bit_position))  # 检查该位是否为 1

            if status[0]:
                self._send_signal_info("硬件错误:Relay: OFF,turn_off_charging_now")
                self.__emergency_shut_down()
            if status[1]:
                self._send_signal_info("硬件错误:Diode check failed,turn_off_charging_now")
                self.__emergency_shut_down()
            if status[2]:
                self._send_signal_info("硬件错误:Vent required fail,turn_off_charging_now")
                self.__emergency_shut_down()
            if status[3]:
                self._send_signal_info(
                    "硬件错误:Waiting for pilot release(error recovery delay),turn_off_charging_now")
                self.__emergency_shut_down()
            if status[4]:
                self._send_signal_info("硬件错误:RCD check error,turn_off_charging_now")
                self.__emergency_shut_down()
            #print("evse_fail_check_end")

    def __clear(self, address, bit):
        # 获取 EVSE 状态
        flag,value,message = self.EVSE.get_EVSE_status_fails()
        # 如果状态失败，检查连接
        if flag == ResultFlag.FAIL:
            self.__handle_connection_error(message)
            return  # 避免继续执行
        # 清除指定位
        value[0] &= ~bit  # 按位清除
        flag, value, message = self.EVSE.write_register(method= 'clear',address= address, value= value)  # 写回寄存器,返回flag

        if flag == ResultFlag.FAIL:
            self.__handle_connection_error(message)
            return

        self._send_signal_info(message)


    def close(self) -> None:
        """关闭连接"""
        self._client.close()
        self._send_signal_info("连接已关闭")

    def __reset_isConeected(self,flag):

        self.__isConnected = flag
        if self.__isConnected:
            self._send_signal_info("重新连接成功")
            self.__checking_connection_thread.stop()


    def set_current(self, current: int) -> bool:
        """
        设置电流，该电流应小于允许值
        会对设置电流的大小做一次判断
        参数:
            - current: Actual configured amps value (from reg 2002 to 80A)
        返回:
            - 成功时返回 True，失败时返回 False
        """
        self.get_vehicle_state()
        if self.__vehicle_state == VehicleState.FAILURE:
            self._send_signal_info("车辆状态异常，无法设置电流")
            return False

        if self.__min_current<= current <= self.__limitCurrent:
            flag,value,message=self.EVSE.write_register(method = 'set_current',address= 1000, value=current)
            #判断是否成功写入
            if flag == ResultFlag.FAIL:
                self.__handle_connection_error(message)
                return False # 避免继续执行
            else:
                if value:
                    current = value[0]
                    self._send_signal_info(f"成功设置电流 {current} A")
        else:
            if current < self.__min_current:
                self._send_signal_info(f"输入电流 {current} A 小于最小限制 {self.__min_current} A")
                return False

            if self.__limitCurrent != 0:
                self._send_signal_info(f"输入电流 {current} A 超过最大限制 {self.__limitCurrent} A")
            else:
                self._send_signal_info("EVSE没有正常连接")
                return False

    def start_polling(self):
        """
        启动定时轮询，定期读取寄存器值并发送
        线程为：
            1. OutputCurrent：轮询当前输出电流
            2. VehicleState：轮询车辆状态
            3. FailCheck：轮询EVSE失效
        """
        if self.__output_current_polling_thread is None:
            self.__output_current_polling_thread = ThreadOutputCurrent(polling_interval=self.__poll_interval,client=self._client)
            self.__output_current_polling_thread.signal_transfer_data.connect(self.send_actual_current)
            self.__output_current_polling_thread.start()
        if self.__vehicle_state_polling_thread is None:
            self.__vehicle_state_polling_thread = ThreadVehicleState(polling_interval=self.__poll_interval_check,client=self._client)
            self.__vehicle_state_polling_thread.signal_transfer_data.connect(self.handle_vehicle_state)
            self.__vehicle_state_polling_thread.start()
        if self.__evse_failure_polling_thread is None:
            self.__evse_failure_polling_thread = ThreadFailCheck(polling_interval=self.__poll_interval,client=self._client)
            self.__evse_failure_polling_thread.signal_transfer_data.connect(self.handle_EVSE_fail)
            self.__evse_failure_polling_thread.start()

    def checking_connection(self):
        
        if self.__checking_connection_thread is None:
            self.__checking_connection_thread = ThreadTryConnection(polling_interval =10, parent = self)
            self.__checking_connection_thread.signal_internal.connect(self.__reset_isConeected)
            self.__checking_connection_thread.start()
        
#完善轮询，present check
    def stop_polling(self):
        """
        停止轮询
        """
        if self.__output_current_polling_thread is not None:
            self.__output_current_polling_thread.stop()
            self.__output_current_polling_thread = None

        if self.__vehicle_state_polling_thread is not None:
            self.__evse_failure_polling_thread.stop()
            self.__evse_failure_polling_thread = None

        if self.__evse_failure_polling_thread is not None:
            self.__evse_failure_polling_thread.stop()
            self.__evse_failure_polling_thread = None


    def __handle_connection_error(self, message):
        """
        统一处理错误逻辑，检查连接并发送错误信息
        """
        self._send_signal_info(message)  # 发送错误消息
        self.checking_connection()  # 检查连接

    def __emergency_shut_down(self):
        self.__Fail = True
        self.signal_EVSE_failure.emit(True)
        self.__turn_off_charging_now()

    def _send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_EVSE_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log= Log.GPIO, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
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
                temp = f'< EVSE_manager >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if doShowTitle:
                error_text = f'< EVSE_manager >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(temp)

# evse = EVSEManager(RCD=False)
# evse.set_current(15)
# evse.set_current(30)
# evse.set_current(3)





