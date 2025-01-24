from _Thread_Shelly_Reader import GetShellyData
from sys_basis.XSignal import XSignal
import requests
from const.Const_Parameter import *
from const.GPIO_Parameter import GPIOParams


_info = Log.GPIO

class ShellyManager:

    def __init__(self, evse_id):
        """
            参数:
                 - __evse_id: 对应的EVSE ID

            信号:
                 -__signal_Shelly_data(dict): Shelly数据,格式如下,列表的0,1,2位代表第1,2,3个电流钳数据

        """
        self.__evse_id = evse_id
        self.__shelly_polling_thread = GetShellyData(self.__evse_id)
        self.__signal_Shelly_error = XSignal()
        self.__signal_Shelly_data = XSignal()
        self.__shelly_polling_thread.signal_Shelly_error.connect(self.signal_Shelly_error.emit)
        self.__shelly_polling_thread.signal_Shelly_data.connect(self.send_data)
        self.__shelly_data = {
            'evse_id': self.__evse_id,
            'shelly_data': {},
            'charged_energy': -1,
        }
        self.__shelly_polling_thread.start()

    @property
    def signal_Shelly_error(self):
        return self.__signal_Shelly_error

    @property
    def signal_Shelly_data(self):
        return self.__signal_Shelly_data

    @property
    def charged_energy(self):
        return self.__shelly_data['charged_energy']


    def reset_total(self):

        try:
            # 发送 POST 请求
            response = requests.post(GPIOParams.SHELLY_IP, timeout=5)
            response.raise_for_status()  # 如果返回状态码不是 2xx, 会抛出异常
            _info("复位成功! ")
        except requests.exceptions.RequestException as e:
            _info(f"复位失败: {e}")

    def send_data(self,data):
        """
        将shelly data发送, 并判断shelly是否正常工作, 如果不正常, 则停止线程
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


        self.__shelly_data['shelly_data'] = data
        self.__shelly_data['charged_energy'] = data["total"][0] + data["total"][1] + data["total"][2]
        self.signal_Shelly_data.emit(self.__shelly_data)

    def close(self):
        self.__shelly_polling_thread.stop()