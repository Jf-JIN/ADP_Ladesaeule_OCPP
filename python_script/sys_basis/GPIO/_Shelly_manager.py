from _Thread_Shelly_Reader import GetShellyData
from sys_basis.XSignal import XSignal
import requests
from const.Const_Parameter import *
from const.GPIO_Parameter import GPIOParams


_info = Log.GPIO

class ShellyManager:

    def __init__(self,new_charge : bool):
        """

            参数:
                 - new_-charge: 根据是否是新的充电来重置total(已充电Wh数)
        """
        self.__new_charge = new_charge
        self.__shelly_polling_thread = GetShellyData()
        self.__signal_Shelly_error = XSignal()
        self.__signal_Shelly_data = XSignal()
        self.__shelly_polling_thread.signal_Shelly_error.connect(self.__signal_Shelly_error.emit)
        self.__shelly_polling_thread.signal_Shelly_data.connect(self.send_data)

        self.reset_total()
        self.__shelly_polling_thread.start()

    @property
    def signal_Shelly_error(self):
        return self.__signal_Shelly_error

    @property
    def signal_Shelly_data(self):
        return self.__signal_Shelly_data


    def reset_total(self):
        if self.__new_charge == True:

            try:
                # 发送 POST 请求
                response = requests.post(GPIOParams.SHELLY_IP, timeout=5)
                response.raise_for_status()  # 如果返回状态码不是 2xx，会抛出异常
                _info("复位成功！")
            except requests.exceptions.RequestException as e:
                _info(f"复位失败: {e}")

        else:
            _info("不是新的充电，不进行复位")

    def send_data(self,data):
        """
        将shelly data分解发送，并判断shelly是否正常工作，如果不正常，则停止线程
        """
        if not isinstance(data, dict):
            self.signal_Shelly_error.emit(True)
            self.__shelly_polling_thread.stop()
            return

        is_valid = data.get("is_valid")

        for i in is_valid:
            if i == False:
                self.signal_Shelly_error.emit(True)
                self.__shelly_polling_thread.stop()
                return

        self.__signal_Shelly_data.emit(data)


