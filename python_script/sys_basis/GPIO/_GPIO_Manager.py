from sys_basis.XSignal import XSignal
from _EVSE_manager import EVSEManager
from _Shelly_manager import ShellyManager
from const.GPIO_Parameter import *
from pymodbus.client import ModbusSerialClient
from _Thread_try_connect import ThreadTryConnection
from _Thread_evse_charge_profile import ThreadChargeProfile
from const.Const_Parameter import *
import threading

class GPIOManager:
    """
    参数:
    - RCD: bool, 是否安装RCD
    - port: 串口端口，默认 '/dev/ttyS0'
    - baudrate: 波特率，默认 9600
    - parity: 有无校验位
    - stopbits: 停止位
    - bytesize: 数据位
    - timeout: 超时时间
    信号:
    -   __signal_GPIO_EVSE_failure: EVSE故障,格式为list[evse_id, bool]
    -   __signal_GPIO_Shelly_error: Shelly故障
    -   __signal_GPIO_Shelly_data: Shelly数据,格式如下,列表的0,1,2位代表第1,2,3个电流钳数据

    方法:
    - set_current: 设置EVSE输出电流
    """
    def __init__(self, port=GPIOParams.PORT, baudrate=GPIOParams.BAUDRATE, parity=GPIOParams.PARITY, stopbits=GPIOParams.STOPBITS, bytesize=GPIOParams.BYTESIZE, timeout=GPIOParams.TIMEOUT,):

        self.__port = port
        self.__baudrate = baudrate
        self.__parity = parity
        self.__stopbits = stopbits
        self.__bytesize = bytesize
        self.__timeout = timeout
        self._client = ModbusSerialClient(
            port=self.__port,  # 串口设备
            baudrate=self.__baudrate,  # 波特率
            parity=self.__parity,  # 无校验位
            stopbits=self.__stopbits,  # 停止位
            bytesize=self.__bytesize,  # 数据位
            timeout=self.__timeout  # 超时时间
        )


        self.__Modbus_isConnected = None
        self.__checking_connection_thread = None

        self.__evse_id_list = [num for num in range(1,GPIOParams.EVSE_QUANTITY+1)]
        self.__evse_instances = {}

        self.__data_dict = { 1:{'evse': {},'shelly': {}},
                           2:{'evse': {},'shelly': {}},
                           3:{'evse': {},'shelly': {}},
                           4:{'evse': {},'shelly': {}},
                           5:{'evse': {},'shelly': {}}
        }

        self.__init_signal_define()
        self.isModbus_Connected()

    def __init_signal_define(self):

        self.__signal_GPIO_EVSE_failure = XSignal()
        self.__signal_GPIO_EVSE_ready = XSignal()
        self.__signal_GPIO_info = XSignal()
        self.__signal_GPIO_data = XSignal()


    @property
    def check_Modbus_connection(self):
        return self.__Modbus_isConnected

    @property
    def signal_GPIO_EVSE_failure(self):
        return self.__signal_GPIO_EVSE_failure

    @property
    def signal_GPIO_EVSE_ready(self):
        return self.__signal_GPIO_EVSE_ready




    def get_GPIO_data(self):
        return self.__data_dict

    def isModbus_Connected(self) -> bool:
        """
        树莓派MODBUS连接状态
        返回:
            - 成功时返回 True，失败时返回 False
        """
        if self._client.connect():
            self._send_signal_info(f"连接成功: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__Modbus_isConnected = True
            return True
        else:
            self._send_signal_info(f"连接失败: 端口={self.__port}, 波特率={self.__baudrate}")
            self.__Modbus_isConnected = False
            self.checking_connection()
            return False

    def checking_connection(self):

        if self.__checking_connection_thread is None:
            self.__checking_connection_thread = ThreadTryConnection(polling_interval=10, parent=self)
            self.__checking_connection_thread.signal_internal.connect(self.__reset_isConeected)
            self.__checking_connection_thread.start()

    def __reset_isConeected(self, flag):

        self.__Modbus_isConnected = flag
        if self.__Modbus_isConnected:
            self._send_signal_info("重新连接成功")
            self.__checking_connection_thread.stop()

    def set_current(self, evse_id, current):
        # 根据 evse_id 找到对应实例并设置电流
        if evse_id in self.__evse_instances:
            self.__evse_instances[evse_id]["evse"].set_current(current)
        else:
            raise ValueError(f"EVSE ID {evse_id} not found")

    def get_ready_evse(self,RCD: bool,):
        #id+init
        if not self.__evse_id_list:
            self._send_signal_info("EVSE ID list is empty, cannot initialize new EVSE")
            return

        new_EVSE_ID = self.__evse_id_list.pop(0)
        evse_instance = EVSEManager(RCD=RCD,evse_id=new_EVSE_ID,client=self._client,)
        shelly_instance = ShellyManager(evse_id = new_EVSE_ID)
        self.__evse_instances[new_EVSE_ID] = {
            "evse": evse_instance,
            "shelly": shelly_instance,
        }
        #车辆连接后发送第一组数据
        self.__evse_instances[new_EVSE_ID]["evse"].signal_EVSE_ready_to_go.connect(self.signal_GPIO_EVSE_ready)
        #其他信号连接
        self.__evse_instances[new_EVSE_ID]["evse"].signal_EVSE_failure.connect(self.signal_GPIO_EVSE_failure.emit)
        self.__evse_instances[new_EVSE_ID]["evse"].send_EVSE_read_write_error.connect(self.isModbus_Connected)
        self.__evse_instances[new_EVSE_ID]["evse"].signal_vehicle_departed.connect(self.kill_evse)
        self.__evse_instances[new_EVSE_ID]["shelly"].signal_Shelly_data.connect(self.__update_shelly_data)
        return


    def kill_evse(self,evse_id):

        self.__evse_instances[evse_id]["evse"].close()
        self.__evse_instances[evse_id]["shelly"].close()
        self.__evse_id_list.append(evse_id)
        

    def _send_signal_info(self, *args) -> None:
            """
            发送/打印 信息信号

            涵盖发送前的检查

            参数:
                - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
            """
            self.__send_signal(signal=self.__signal_GPIO_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

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
                temp = f'< GPIO_manager >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if doShowTitle:
                error_text = f'< GPIO_manager >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(temp)
