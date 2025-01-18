import traceback
from const.GPIO_Parameter import GPIOParams
import requests
from sys_basis.XSignal  import XSignal
from threading import Thread
from const.Const_Parameter import *
import time

_info = Log.GPIO

class GetShellyData(Thread):

    def __init__(self,evse_id):
        super().__init__()
        self.__interval = GPIOParams.POLL_INTERVAL_SHELLY  # 每隔多少秒返回时间
        self.__running = True  # 控制线程是否继续运行
        self.__Signal_Shelly_data = XSignal()
        self.__Signal_Shelly_error = XSignal()
    # 替换为实际的 Shelly 3EM 设备 IP 地址
        self.__shelly_ip = GPIOParams.SHELLY_IP[evse_id]
        self.__emeter_0_url = f"http://{self.__shelly_ip}/emeter/0"
        self.__emeter_1_url = f"http://{self.__shelly_ip}/emeter/1"
        self.__emeter_2_url = f"http://{self.__shelly_ip}/emeter/2"

    @property
    def signal_Shelly_data(self) -> XSignal:
        return self.__Signal_Shelly_data

    @property
    def signal_Shelly_error(self) -> XSignal:
        return self.__Signal_Shelly_error

    def get_data(self):
        try:
            #请求失败后的处理
            current_clamp_1 = requests.get(self.__emeter_0_url, timeout=5)
            current_clamp_1.raise_for_status()
            data_1 = current_clamp_1.json()
            current_clamp_2 = requests.get(self.__emeter_1_url, timeout=5)
            current_clamp_2.raise_for_status()
            data_2 = current_clamp_2.json()
            current_clamp_3 = requests.get(self.__emeter_2_url, timeout=5)
            current_clamp_3.raise_for_status()
            data_3 = current_clamp_3.json()

            merged_data = {key: [data_1[key], data_2[key], data_3[key]] for key in data_1.keys()}
            _info(f"汇总的电能数据：", merged_data)
            return merged_data
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