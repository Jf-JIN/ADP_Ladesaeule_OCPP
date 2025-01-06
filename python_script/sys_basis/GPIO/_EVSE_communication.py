from pymodbus.client import ModbusSerialClient
import time
import threading
from typing import Optional, List
from pymodbus import ModbusException
from XSignal import XSignal
from thread00 import T1
from _Thread_evse_try_connect import TryConnection 
from GPIO_Parameter import GPIOParams

class EVSECommunication:



    def __init__(self, port=GPIOParams.PORT, baudrate=GPIOParams.BAUDRATE, poll_interval=GPIOParams.POLL_INTERVAL, poll_interval_check= GPIOParams.POLL_INTERVAL_CHECK,
                 parity=GPIOParams.PARITY, stopbits=GPIOParams.STOPBITS, bytesize=GPIOParams.BYTESIZE, timeout=GPIOParams.TIMEOUT):
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
        """

        self.__port = port
        self.__baudrate = baudrate               
        self.__poll_interval= poll_interval
        self.__poll_interval_check= poll_interval_check
        self.__parity = parity
        self.__stopbits = stopbits
        self.__bytesize = bytesize
        self.__timeout = timeout

        self.__loop_polling_thread = None
        self.__check_polling_thread = None
        self.__checking_connection_thread = None
        self.__isConnected = False
        self._client = ModbusSerialClient(
            port=self.__port,        # 串口设备
            baudrate=self.__baudrate,  # 波特率
            parity=self.__parity,             # 无校验位
            stopbits=self.__stopbits,             # 停止位
            bytesize=self.__bytesize,             # 数据位
            timeout=self.__timeout               # 超时时间
        )
        self.__signal_EVSE_info = XSignal()
        self.__signal_EVSE_data = XSignal()
        self.__signal_EVSE_failure = XSignal()
        self.__vehicle_state = [0,'ready','EV is present','charging','charging with ventilation','failure (e.g. diode check, RCD failure)']#get_vehicle_state返回1~5，0用于占位
        self.__EVSE_state = [0,'steady 12V','PWM is being generated(only if 1000 >= 6)','OFF, steady 12V']
        self.booting()

    @property
    def signal_EVSE_data(self):
        return self.__signal_EVSE_data

    @property
    def signal_EVSE_failure(self):
        return self.__signal_EVSE_failure

    def booting(self):
        if self.isConnected():
            allowed_current = self.get_allowed_current()
            vehicle_state =self.__vehicle_state[self.get_vehicle_state()[0]]
            if allowed_current:
                self.__send_signal_info(f"允许最大电流为{allowed_current}A")
                self.__limitCurrent = allowed_current  # 获取允许的电流值
            else:
                self.__send_signal_info("获取允许电流失败")
                self.__limitCurrent = 0  # 设置默认值或其他处理方式
            if vehicle_state:
                self.__send_signal_info(f"车辆状态为{vehicle_state}")
            else:
                self.__send_signal_info("获取车辆状态失败")
        else:
            self.__limitCurrent = 0  # 如果连接失败，设置默认值

        self.__clear_RCD_error()
        self.__clear_turn_off_charging()
        self.__run_selftest_and_RCD_test_procedure()

    def isConnected(self) -> bool:
        """
        是否连接到设备
        返回:
            - 成功时返回 True，失败时返回 False
        """
        if self._client.connect():
            self.__send_signal_info(f"连接成功: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__isConnected = True
            return True
        else:
            self.__send_signal_info(f"连接失败: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__isConnected = False
            return False

    def close(self) -> None:
        """关闭连接"""
        self._client.close()
        self.__send_signal_info("连接已关闭")

    def __reset_isConeected(self,flag):

        self.__isConnected = flag

    def get_allowed_current(self) -> Optional[int]:
        """
         6 / 13 / 20 / 32 / 63 / 80 A
         Maximum current limitation according to a cable based on PP
         resistor detection
        返回:
            - 成功时返回允许值并发送，失败时返回 None
        """
        allowed_current = self.read_register(address=1003)[0]
        self.signal_EVSE_data.emit(allowed_current)
        return allowed_current

    def get_actual_current(self) -> Optional[int]:
        """
         Actual amps value output
        返回:
            - 成功时返回电流值并发送，失败时返回 None
        """
        actual_current = self.read_register(address=1001)[0]
        self.signal_EVSE_data.emit(actual_current)
        return actual_current

    def get_vehicle_state(self) -> Optional[List[int]]:
        """
        Vehicle state:
            1: ready
            2: EV is present
            3: charging
            4: charging with ventilation
            5: failure (e.g. diode check, RCD failure)
        返回:
            - 成功时返回寄存器值列表，失败时返回 None
        """
        return self.read_register(address=1002)

    def get_EVSE_state(self) -> Optional[List[int]]:
        """
        EVSE state
            1: steady 12V
            2: PWM is being generated(only if 1000 >= 6)
            3: OFF, steady 12V
        返回:
            - 成功时返回寄存器值列表，失败时返回 None
        """
        self.__send_signal_info(self.__EVSE_state[self.read_register(address=1006)[0]])
        return self.read_register(address=1006)

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
        result = self.read_register(address=1007)
        if result and isinstance(result, list):
            state_value = result[0]  # 安全取出第一个值
        else:
            self.__send_signal_info("get_EVSE_status_fails返回值为空")
            return None
        status_map = {
            0: "Relay: ON" if state_value & (1 << 0) else "Relay: OFF",
            1: "Diode check failed" if state_value & (1 << 1) else "safe",
            2: "Vent required fail" if state_value & (1 << 2) else "safe",
            3: "Waiting for pilot release(error recovery delay)" if state_value & (1 << 3) else "safe",
            4: "RCD check error" if state_value & (1 << 4) else "RCD check passed",
            5: "Reserved (bit5)",
            6: "Reserved (bit6)",
            # Add additional bits if needed
            # 7 to 15: Reserved by specification
        }
        # 将状态转换为字符串并发送
        info = "\n".join(f"Bit {bit}: {desc}" for bit, desc in status_map.items())
        self.__send_signal_info(info)

        status = {}
        for bit_position in status_map.keys():
            status[bit_position] = bool(state_value & (1 << bit_position))  # 检查该位是否为 1

        # 根据结果中断充电并发送信息
        if status[0]:
            self.__turn_off_charging_now()
            self.__send_signal_info("硬件错误:Relay: OFF,turn_off_charging_now")
            self.signal_EVSE_failure.emit(True)
        if status[1]:
            self.__turn_off_charging_now()
            self.__send_signal_info("硬件错误:Diode check failed,turn_off_charging_now")
            self.signal_EVSE_failure.emit(True)
        if status[2]:
            self.__turn_off_charging_now()
            self.__send_signal_info("硬件错误:Vent required fail,turn_off_charging_now")
            self.signal_EVSE_failure.emit(True)
        if status[3]:
            self.__turn_off_charging_now()
            self.__send_signal_info("硬件错误:Waiting for pilot release(error recovery delay),turn_off_charging_now")
            self.signal_EVSE_failure.emit(True)
        if status[4]:
            self.__turn_off_charging_now()
            self.__send_signal_info("硬件错误:RCD check error,turn_off_charging_now")
            self.signal_EVSE_failure.emit(True)

    def set_current(self,current : int) -> bool:
        """
        设置电流，该电流应小于允许值
        会对设置电流的大小做一次判断
        对车辆状态做一次判断
        参数:
            - current: Actual configured amps value (from reg 2002 to 80A)
        返回:
            - 成功时返回 True，失败时返回 False
        """
        if self.get_vehicle_state()[0] == 5:
            self.__send_signal_info("车辆状态错误")
            return False
        else:
            if current < self.__limitCurrent:
                self.__write_register(1000, value = current)
                return True
            else:
                if self.__limitCurrent != 0 :
                    self.__send_signal_info(f"输入电流 {current} A 超过最大限制 {self.__limitCurrent} A")
                else:
                    self.__send_signal_info("EVSE没有正常连接")
                return False

    def __turn_off_charging_now(self) -> bool:
        result = self.__write_register(1004, value=0b00000001)
        if result:
            self.__send_signal_info("充电已停止")
            return True
        else:
            self.__send_signal_info("停止充电失败")
            return False

    def __clear_turn_off_charging(self):
        result = self.__write_register(1004, value=0b00000000)
        if result:
            self.__send_signal_info("已清除禁止充电状态")
            return True
        else:
            self.__send_signal_info("清除禁止充电状态失败")
            return False


    def __run_selftest_and_RCD_test_procedure(self):
        result = self.__write_register(1004, value=0b00000010)
        if result:
            self.__send_signal_info("run selftest and RCD test procedure (approx 30s)")
            return True
        else:
            self.__send_signal_info("selftest and RCD test procedure failed")
            return False

    def __clear_RCD_error(self):
        result = self.__write_register(1004, value=0b00000100)
        if result:
            self.__send_signal_info("clear RCD error")
            return True
        else:
            self.__send_signal_info("clear RCD error failed")
            return False

    def start_polling(self):
        """
        启动定时轮询，定期读取寄存器值并发送
        """
        if self.__loop_polling_thread is None:
            self.__loop_polling_thread = T1(5)
            #连接信号
            self.__loop_polling_thread.start()
        if self.__check_polling_thread is None:
            self.__check_polling_thread = T1(5)#新建检查线程
            # 连接信号
            self.__check_polling_thread.start()
    
    def checking_connection(self):
        
        if self.__checking_connection_thread is None:
            self.__checking_connection_thread = TryConnection(polling_interval =10, parent = self)
            self.__checking_connection_thread.signal_internal.connect(self.__reset_isConeected)
            self.__checking_connection_thread.start()
        
#完善轮询，present check
    def stop_polling(self):
        """
        停止轮询
        """
        self.__polling_thread = None

    def finished_loop_polling(self):
        self.__loop_polling_thread.stop()
        self.__loop_polling_thread = None


    def __polling_loop(self):
        """
        轮询循环，每隔一定时间读取寄存器并发送信息
        """
        while self.__polling_thread is not None:
            self.poll_and_send()
            time.sleep(self.__poll_interval)  # 等待指定的轮询间隔

    def __polling_check(self):
        """
        轮询循环，每隔一定时间检查是否拔出充电头
        """
        while self.__polling_thread is not None:
            self.poll_and_send()
            time.sleep(self.__poll_interval_check)  # 等待指定的轮询间隔

    def poll_and_send(self):
        """
        读取寄存器并发送信号
        """

        current_values = self.read_register(address=1003)  # 示例：读取地址为 1003 的寄存器
        if current_values:
            self.__send_signal_info(f"读取到的电流值: {current_values}")
        else:
            self.__send_signal_info("无法读取电流值")

    def read_register(self, address: int, count: int = 1, slave: int = 1) -> Optional[List[int]]:
        """
        读取保持寄存器（Holding Registers）
        参数:
            - address: 起始寄存器地址（零偏移）
            - count: 读取的寄存器数量，默认为 1
            - slave: 从站地址，EVSE 从站地址为 1
        返回
            - 成功时返回寄存器值列表，失败时返回 None(pymodbus要求返回None)
        """
        try:
            # 读取寄存器
            result = self._client.read_holding_registers(address=address, count=count, slave=slave)
        except ModbusException as e:
            self.__send_signal_info(f"发送或接收数据时发生 Modbus 错误: {e}")
            self.checking_connection()  # 启动连接检查
            return None
        except Exception as e:
            self.__send_signal_info(f"发送或接收数据时发生未知错误: {e}")
            self.checking_connection()  # 启动连接检查
            return None

            # 处理读取结果
        if not result.isError():
            self.__send_signal_info(f"成功读取到 {count} 个寄存器，从地址 {address} 开始: {result.registers}")
            return result.registers
        else:
            self.__send_signal_info(f"读取错误，功能码返回错误或无效响应: {result}")
            self.checking_connection()  # 启动连接检查
            return None

    def __write_register(self, address: int, value: int, slave: int = 1) -> Optional[bool]:
        """
        写入一个保持寄存器（Holding Register）
        参数:
            - address: 寄存器地址
            - value: 要写入的值
            - slave: 从站地址，默认值为 1
        返回:
            - 成功时返回 True，失败时返回 False
        """
        try:
            # 将值封装成列表，因为 pymodbus 的 write_registers 接收列表
            rq = self._client.write_registers(address=address, values=[value], slave=slave)

        except ModbusException as e:
               # 捕获 Modbus 异常
               self.__send_signal_info(f"发送或接收数据时发生 Modbus 错误: {e}")
               self.checking_connection()  # 启动连接检查
               return False
        except Exception as e:
               # 捕获其他非 Modbus 异常
               self.__send_signal_info(f"发送或接收数据时发生未知错误: {e}")
               self.checking_connection()  # 启动连接检查
               return False

        if not rq.isError():
            self.__send_signal_info(f"成功写入寄存器 {address}，值为 {value}")
            return True
        else:
            self.__send_signal_info(f"写入失败，寄存器 {address}，值为 {value}")
            self.checking_connection()  # 启动连接检查
            return False

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_EVSE_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
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




