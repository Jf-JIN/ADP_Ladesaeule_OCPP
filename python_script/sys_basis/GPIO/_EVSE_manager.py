import time
from time import sleep
from typing import Optional
from _Decorator_check_flag import check_flag
from const.GPIO_Parameter import *
from const.Const_Parameter import *

from sys_basis.XSignal import XSignal
from sys_basis.GPIO._evse_r_w import EVSEReadWrite
#from sys_basis.GPIO._evse_r_w_test import EVSEReadWrite
from _Thread_evse_output_current import ThreadOutputCurrent
from _Thread_evse_fail_check import ThreadFailCheck
from _Thread_evse_vehicle_state import ThreadVehicleState



class EVSEManager(object):

    def __init__(self, RCD: bool, evse_id: int, client, poll_interval=GPIOParams.POLL_INTERVAL, poll_interval_check= GPIOParams.POLL_INTERVAL_CHECK,):
        """
        初始化通信对象，设置串口参数
        参数:
             - RCD: 是否使用RCD
             - evse_id: 分配的EVSE id
             - poll_interval: 读取数据的间隔时间，默认 5 秒
             - poll_interval_check: 检查充电头是否拔出，默认 1 秒
        """

        self.__output_current_polling_thread = None
        self.__vehicle_state_polling_thread = None
        self.__evse_failure_polling_thread = None
        self.__poll_interval = poll_interval
        self.__poll_interval_check = poll_interval_check

        self.__isRCD = RCD
        self.__evse_data = {
            'EVSE_ID': evse_id,
            'min_current': -1,
            'allowed_current': -1,
            'actual_current': -1,
            'target_energy': -1,
            'remaining_to_charge': -1,
            'planed_depart_time': -1,
            'vehicle_state': 'No value',
            'EVSE_Failure': False,
            'EVSE_selftest_Fail': False,
        }

        self._client = client

        self.__signal_EVSE_info = XSignal()
        self.__signal_EVSE_read_write_error = XSignal()
        self.__signal_EVSE_ready_to_go = XSignal()
        self.__signal_vehicle_departed = XSignal()
        self.__signal_EVSE_failure = XSignal()
        
        self.__vehicle_state_list = [0, 'ready', 'EV is present', 'charging', 'charging with ventilation','failure (e.g. diode check, RCD failure)']  # get_vehicle_state返回1~5，0用于占位
        self.__current_vehicle_state = None
        self.__previous_vehicle_state = None
        self.__EVSE_state_list = [0,'steady 12V','PWM is being generated(only if 1000 >= 6)','OFF, steady 12V']
        self.EVSE = EVSEReadWrite(client= self._client, evse_id=self.__evse_data['evse_id'])
        self.booting()


    @property
    def signal_vehicle_departed(self):
        return self.__signal_vehicle_departed

    @property
    def signal_EVSE_ready_to_go(self):
        return self.__signal_EVSE_ready_to_go

    @property
    def get_id(self):
        return self.__evse_data['evse_id']

    @property
    def get_evse_data(self):
        return self.__evse_data

    @property
    def send_EVSE_read_write_error(self):
        return self.__signal_EVSE_read_write_error.emit(True)

    @property
    def signal_EVSE_failure(self):
        return self.__signal_EVSE_failure

    def booting(self):

        if self.__isRCD:
            self.enable_RCD()

        self.__clear(address=1004,bit=REG1004.TURN_OFF_CHARGING_NOW)

        self.selftest()
        if not self.__evse_data['EVSE_Failure'] :
            self.start_polling()

            self.wait_for_EV()

            self.__evse_data['allowed_current'] = self.get_allowed_current()
            self.__evse_data['min_current']= self.get_min_current()
            if self.__evse_data['allowed_current']>=0:
                self._send_signal_info(f"允许最大电流为{self.__evse_data['allowed_current']}A")
            else:
                self._send_signal_info("获取允许电流失败")

            if self.__evse_data['min_current']>=0:
                self._send_signal_info(f"允许最小电流为{self.__evse_data['min_current']}A")
            else:
                self._send_signal_info("获取最小电流失败")

            if self.__evse_data['min_current'] == -1 or self.__evse_data['allowed_current'] == -1:
                self.send_EVSE_read_write_error()
                self._send_signal_info('Booting:读写错误')
                return
            else:
                self._send_signal_info('Booting:成功')
                self.signal_EVSE_ready_to_go.emit(self.__evse_data)
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
                self.send_EVSE_read_write_error()
                self._send_signal_info(message)
            # 如果包含 RCD_CHECK_ERROR，清除错误
            elif value & EVSEFails.RCD_CHECK_ERROR:
                self.__clear(address=1007, bit=EVSEFails.RCD_CHECK_ERROR)

            else:
                self.__evse_data['EVSE_selftest_Fail'] = True
                self.__evse_data['EVSE_Failure'] = True
                self._send_signal_info("RCD failed to alarm")
                self.signal_EVSE_failure.emit([self.__evse_data['evse_id'],True])

        self.handle_EVSE_fail(self.EVSE.get_EVSE_status_fails())

    def wait_for_EV(self):
        while True:
           current_vehicle_state = self.__vehicle_state
           self._send_signal_info("waiting for EV...")
           if current_vehicle_state == VehicleState.EV_IS_PRESENT:
               self._send_signal_info("EV is present")
           break
        time.sleep(1)


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
            self.__evse_data['allowed_current'] = value[0]
        else:
            self.__evse_data['allowed_current'] = -1
        self._send_signal_info(message)
        return self.__evse_data['allowed_current']

    @check_flag(used_method =lambda self: self.EVSE.get_vehicle_state())
    def get_vehicle_state(self,value,message) -> int:
        """
        检查flag,获取并改变车辆状态,并赋值给self.__vehicle_state
        返回:
            - 成功时返回 self.__vehicle_state，失败时返回 None
        """
        if value:
            self.__vehicle_state = value[0]
            self.__evse_data['vehicle_state'] = self.__vehicle_state_list[self.__vehicle_state]
            self.update_state(self.__vehicle_state)
        else:
            self.__vehicle_state = None
        self._send_signal_info(message)
        return self.__vehicle_state

    def update_state(self, new_state):
        if new_state == VehicleState.READY and self.__previous_vehicle_state in {VehicleState.EV_IS_PRESENT, VehicleState.CHARGING, VehicleState.CHARGING_WITH_VENTILATION}:
            self.__turn_off_charging_now()
            self.signal_vehicle_departed.emit(self.__evse_data['evse_id'])
        __previous_vehicle_state = self.__current_vehicle_state
        self.__current_vehicle_state = new_state

    @check_flag(used_method =lambda self: self.EVSE.get_min_current())
    def get_min_current(self,value,message) -> int:
        """
              检查flag,获取最低电流
              返回:
                  - 成功时返回 self.__evse_data['min_current']，失败时返回 -1
              """
        if value:
            self.__evse_data['min_current'] = value[0]
        else:
            self.__evse_data['min_current'] = -1
        self._send_signal_info(message)

        return self.__evse_data['min_current']

    def send_actual_current(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.send_EVSE_read_write_error()
            self._send_signal_info(message)
        else:
            self.__evse_data['actual_current'] = value[0]

            #print(f'测试{actual_current}A')

    def handle_vehicle_state(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.send_EVSE_read_write_error()
            self._send_signal_info(message)
        else:
            self.__vehicle_state = value[0]
            if self.__vehicle_state == VehicleState.FAILURE:
                self.__emergency_shut_down()
                self._send_signal_info(f'车辆状态异常，已紧急断电')
            self.__evse_data['vehicle_state'] = self.__vehicle_state_list[self.__vehicle_state]

    def handle_EVSE_fail(self,data):
        flag, value, message = data
        if flag == ResultFlag.FAIL:
            self.send_EVSE_read_write_error()
            self._send_signal_info(message)
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
            self.send_EVSE_read_write_error()
            self._send_signal_info(message)
            return  # 避免继续执行
        # 清除指定位
        value[0] &= ~bit  # 按位清除
        flag, value, message = self.EVSE.write_register(method= 'clear',address= address, value= value)  # 写回寄存器,返回flag

        if flag == ResultFlag.FAIL:
            self.send_EVSE_read_write_error()
            self._send_signal_info(message)
            return

        self._send_signal_info(message)

    def close(self) -> None:
        """关闭连接"""
        self.stop_polling()
        self.__turn_off_charging_now()
        self._send_signal_info(f"id为{self.__evse_data['EVSE_ID']}的实例已关闭")

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
        if self.__vehicle_state == VehicleState.READY:
            self._send_signal_info("车辆未连接，无法设置电流")
            return False

        if self.__evse_data['min_current']<= current <= self.__evse_data['allowed_current']:
            flag,value,message=self.EVSE.write_register(method = 'set_current',address= 1000, value=current)
            #判断是否成功写入
            if flag == ResultFlag.FAIL:
                self.send_EVSE_read_write_error()
                self._send_signal_info(message)
                return False # 避免继续执行
            else:
                if value:
                    current = value[0]
                    self._send_signal_info(f"成功设置电流 {current} A")
        else:
            if current < self.__evse_data['min_current']:
                self._send_signal_info(f"输入电流 {current} A 小于最小限制 {self.__evse_data['min_current']} A")
                return False

            if self.__evse_data['allowed_current'] != -1:
                self._send_signal_info(f"输入电流 {current} A 超过最大限制 {self.__evse_data['allowed_current']} A")
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
            self.__output_current_polling_thread = ThreadOutputCurrent(polling_interval=self.__poll_interval, client=self._client, evse_id=self.__evse_data['evse_id'])
            self.__output_current_polling_thread.signal_transfer_data.connect(self.send_actual_current)
            self.__output_current_polling_thread.start()
        if self.__vehicle_state_polling_thread is None:
            self.__vehicle_state_polling_thread = ThreadVehicleState(polling_interval=self.__poll_interval_check, client=self._client, evse_id=self.__evse_data['evse_id'])
            self.__vehicle_state_polling_thread.signal_transfer_data.connect(self.handle_vehicle_state)
            self.__vehicle_state_polling_thread.start()
        if self.__evse_failure_polling_thread is None:
            self.__evse_failure_polling_thread = ThreadFailCheck(polling_interval=self.__poll_interval, client=self._client, evse_id=self.__evse_data['evse_id'])
            self.__evse_failure_polling_thread.signal_transfer_data.connect(self.handle_EVSE_fail)
            self.__evse_failure_polling_thread.start()

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


    # def __handle_connection_error(self, message):
    #     """
    #     统一处理错误逻辑，检查连接并发送错误信息
    #     """
    #     self._send_signal_info(message)  # 发送错误消息
    #     self.checking_connection()  # 检查连接

    def __emergency_shut_down(self):
        self.__evse_data['EVSE_Failure']= True
        self.signal_EVSE_failure.emit([self.__evse_data['evse_id'],True])
        self.__turn_off_charging_now()

    def _send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_EVSE_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log= Log.GPIO.info, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
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





