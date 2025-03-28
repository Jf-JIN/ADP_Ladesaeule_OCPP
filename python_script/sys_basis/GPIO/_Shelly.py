
import copy
from const.Const_Parameter import *
import requests
from sys_basis.XSignal import XSignal

_info = Log.GPIO


class Shelly:
    def __init__(self, id: int, address: str) -> None:
        self.__id: int = id
        self.__main_address: str = address
        self.__data: dict = {}
        self.__isAvailable: bool = False
        self.__charged_energy: int = 0
        self.__signal_current_no = XSignal()
        self.__signal_current_overload = XSignal()
        self.__signal_shelly_error_occurred = XSignal()
        self.__signal_charged_energy = XSignal()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def main_address(self) -> str:
        return self.__main_address

    @property
    def sub_address_0(self) -> str:
        if self.__main_address.startswith('http'):
            return f"{self.__main_address}/emeter/0"
        else:
            return f"http://{self.__main_address}/emeter/0"

    @property
    def sub_address_1(self) -> str:
        if self.__main_address.startswith('http'):
            return f"{self.__main_address}/emeter/1"
        else:
            return f"http://{self.__main_address}/emeter/1"

    @property
    def sub_address_2(self) -> str:
        if self.__main_address.startswith('http'):
            return f"{self.__main_address}/emeter/2"
        else:
            return f"http://{self.__main_address}/emeter/2"

    @property
    def address_list(self) -> list:
        return copy.deepcopy([self.sub_address_0, self.sub_address_1, self.sub_address_2])

    @property
    def isAvailable(self) -> bool:
        return self.__isAvailable

    @property
    def charged_energy(self) -> int | float:
        return self.__charged_energy

    @property
    def data(self) -> dict:
        return copy.deepcopy(self.__data)

    @property
    def data_ph0(self) -> dict:
        return copy.deepcopy(self.__data[0])

    @property
    def data_ph1(self) -> dict:
        return copy.deepcopy(self.__data[1])

    @property
    def data_ph2(self) -> dict:
        return copy.deepcopy(self.__data[2])

    @property
    def signal_shelly_error_occurred(self) -> XSignal:
        return self.__signal_shelly_error_occurred

    @property
    def signal_current_no(self) -> XSignal:
        return self.__signal_current_no

    @property
    def signal_current_overload(self) -> XSignal:
        return self.__signal_current_overload

    @property
    def signal_charged_energy(self) -> XSignal:
        return self.__signal_charged_energy

    def set_data(self, data: dict) -> None:
        self.__data = data
        self.__charged_energy = self.__data['charged_energy']
        self.__isAvailable = self.__data['is_valid']
        charged_energy = self.__data['charged_energy']
        if not self.__isAvailable:
            self.signal_shelly_error_occurred.emit(not self.__isAvailable)
            return
        self.signal_charged_energy.emit(charged_energy)

    def reset(self) -> None:
        _info('Shelly reset')
        try:
            # 发送 POST 请求
            reset_token = 'reset_totals'
            response0 = requests.post(f"{self.sub_address_0}/{reset_token}", timeout=5)
            response0.raise_for_status()
            response1 = requests.post(f"{self.sub_address_1}/{reset_token}", timeout=5)
            response1.raise_for_status()
            response2 = requests.post(f"{self.sub_address_2}/{reset_token}", timeout=5)
            response2.raise_for_status()
            _info("Shelly 复位成功\nShelly reset successfully")
        except requests.exceptions.RequestException as e:
            _info(f"Shelly 复位失败\nShelly reset failed: {e}")
