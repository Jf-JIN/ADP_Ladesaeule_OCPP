import traceback
from const.GPIO_Parameter import GPIOParams
import requests
from sys_basis.XSignal  import XSignal
from threading import Thread
from const.Const_Parameter import *
import time

_info = Log.GPIO

class GetShellyData(Thread):

    def __init__(self):
        super().__init__()
        self.__interval = GPIOParams.POLL_INTERVAL_SHELLY  # 每隔多少秒返回时间
        self.__running = True  # 控制线程是否继续运行
        self.__Signal_Shelly_data = XSignal()
        self.__Signal_Shelly_error = XSignal()
    # 替换为实际的 Shelly 3EM 设备 IP 地址
        self.__shelly_ip = GPIOParams.SHELLY_IP
        self.__emeter_index = GPIOParams.SHELLY_EMETER_INDEX
        self.__emeter_url = f"http://{self.__shelly_ip}/emeter/{self.__emeter_index}"

    @property
    def signal_Shelly_data(self) -> XSignal:
        return self.__Signal_Shelly_data

    @property
    def signal_Shelly_error(self) -> XSignal:
        return self.__Signal_Shelly_error

    def get_data(self):
        try:
            #请求失败后的处理
            response = requests.get(self.__emeter_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            _info(f"通道 {self.__emeter_index} 的电能数据：", data)
            return data
        except requests.exceptions.RequestException as e:
            _info(f"请求失败: {traceback.format_exc()}")
            self.signal_Shelly_error.emit(True)
            return None

    def run(self):
        while self.__running:
            data = self.get_data()
            if data:
                self.signal_Shelly_data.emit(data)
                _info(f"Shelly数据：{data}")
            time.sleep(self.__interval)

    def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束