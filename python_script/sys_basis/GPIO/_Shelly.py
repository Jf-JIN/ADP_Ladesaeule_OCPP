
import copy
from const.GPIO_Parameter import GPIOParams
from const.Const_Parameter import *
import requests
from sys_basis.XSignal  import XSignal

_info = Log.GPIO

class Shelly:
    def __init__(self,id:int,address:str):
        self.__id:int = id
        self.__main_address:str = address
        self.__data:dict = {}
        self.__isAvailable:bool = True
        self.__charged_energy:int = 0
        self.__signal_current_no = XSignal()
        self.__signal_current_overload = XSignal()
        self.__signal_shelly_error_occured = XSignal()
        self.__sub_address_0 = f"http://{self.__main_address}/emeter/0"
        self.__sub_address_1 = f"http://{self.__main_address}/emeter/1"
        self.__sub_address_2 = f"http://{self.__main_address}/emeter/2"


    @property
    def id(self):
        return self.__id

    @property
    def main_address(self):
        return self.__main_address

    @property
    def sub_address_0(self):
        return self.__sub_address_0

    @property
    def sub_address_1(self):
        return self.__sub_address_1

    @property
    def sub_address_2(self):
        return self.__sub_address_2

    @property
    def address_list(self):
        return copy.deepcopy([self.__sub_address_0, self.__sub_address_1, self.__sub_address_2])

    @property
    def isAvailable(self):
        return self.__isAvailable

    @property
    def charged_energy(self):
        return self.__charged_energy

    @property
    def data(self):
        return copy.deepcopy(self.__data)

    @property
    def data_ph0(self):
        return copy.deepcopy(self.__data[0])

    @property
    def data_ph1(self):
        return copy.deepcopy(self.__data[1])

    @property
    def data_ph2(self):
        return copy.deepcopy(self.__data[2])

    @property
    def signal_shelly_error_occured(self):
        return self.__signal_shelly_error_occured

    def set_data(self, data:dict):
        self.__data = data
        self.__charged_energy = self.__data['charged_energy']
        self.__isAvailable = self.__data['is_valid']
        if not self.__isAvailable:
            self.signal_shelly_error_occured.emit()

    def reset(self):
        try:
            # 发送 POST 请求
            reset_token = 'reset_totals'
            response0 = requests.post(f"{self.__sub_address_0}/{reset_token}", timeout=5)
            response0.raise_for_status()
            response1 = requests.post(f"{self.__sub_address_1}/{reset_token}", timeout=5)
            response1.raise_for_status()
            response2 = requests.post(f"{self.__sub_address_2}/{reset_token}", timeout=5)
            response2.raise_for_status()
            _info("复位成功! ")
        except requests.exceptions.RequestException as e:
            _info(f"复位失败: {e}")


