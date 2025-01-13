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
        self.__signal_Shelly_power = XSignal()
        self.__signal_Shelly_pf = XSignal()
        self.__signal_Shelly_current = XSignal()
        self.__signal_Shelly_voltage = XSignal()
        self.__signal_Shelly_is_valid = XSignal()
        self.__signal_Shelly_total = XSignal()
        self.__signal_Shelly_total_returned = XSignal()
        self.__shelly_polling_thread.signal_Shelly_error.connect(self.__signal_Shelly_error.emit)
        self.__shelly_polling_thread.signal_Shelly_data.connect(self.send_data)

        self.reset_total()
        self.__shelly_polling_thread.start()

    @property
    def signal_Shelly_error(self):
        return self.__signal_Shelly_error

    @property
    def signal_Shelly_power(self):
        return self.__signal_Shelly_power

    @property
    def signal_Shelly_pf(self):
        return self.__signal_Shelly_pf

    @property
    def signal_Shelly_current(self):
        return self.__signal_Shelly_current

    @property
    def signal_Shelly_voltage(self):
        return self.__signal_Shelly_voltage

    @property
    def signal_Shelly_is_valid(self):
        return self.__signal_Shelly_is_valid

    @property
    def signal_Shelly_total(self):
        return self.__signal_Shelly_total

    @property
    def signal_Shelly_total_returned(self):
        return self.__signal_Shelly_total_returned

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

        power = data.get("power")
        pf = data.get("pf")
        current = data.get("current")
        voltage = data.get("voltage")
        is_valid = data.get("is_valid")
        total = data.get("total")
        total_returned = data.get("total_returned")

        if is_valid == False:
            self.signal_Shelly_error.emit(True)
            self.__shelly_polling_thread.stop()
            return

        self.__signal_Shelly_power.emit(power)
        self.__signal_Shelly_pf.emit(pf)
        self.__signal_Shelly_current.emit(current)
        self.__signal_Shelly_voltage.emit(voltage)
        self.__signal_Shelly_total.emit(total)
        self.__signal_Shelly_total_returned.emit(total_returned)

