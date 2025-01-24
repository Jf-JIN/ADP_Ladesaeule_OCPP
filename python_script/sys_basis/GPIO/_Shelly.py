#!/usr/bin/python
# -*- coding: utf-8 -*-
from const.GPIO_Parameter import GPIOParams
from const.Const_Parameter import *
import requests
from sys_basis.XSignal  import XSignal
from _Polling_Shelly import PollingShelly

_info = Log.GPIO

class Shelly:
    def __init__(self,id):

        #
        self.address_list = None
        #
        #self.signal_current_no = None
        #self.signal_current_overload = None
        self.__id = None
        self.__main_address = GPIOParams.SHELLY_IP[self.__id]
        self.__data = {}
        self.__isAvailable = None
        self.__charged_energy = None
        #self.__signal_current_no = None
        #self.__signal_current_overload = None
        self.__signal_shelly_error_occured = None
        self.__sub_address_0 = f"http://{self.__main_address}/emeter/0"
        self.__sub_address_1 = f"http://{self.__main_address}/emeter/1"
        self.__sub_address_2 = f"http://{self.__main_address}/emeter/2"
        self.shelly = PollingShelly


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
    def isAvailable(self):
        return self.__isAvailable

    @property
    def charged_energy(self):
        return self.__charged_energy

    @property
    def data(self):
        return self.__data

    @property
    def data_ph0(self):
        return self.__data['0']

    @property
    def data_ph1(self):
        return self.__data['1']

    @property
    def data_ph2(self):
        return self.__data['2']

    @property
    def signal_shelly_error_occured(self):
        return self.__signal_shelly_error_occured.emit(True)



    def set_data(self, data):
        self.__data = data
        self.__charged_energy = self.__data['0']['total'] + self.__data['1']['total'] + self.__data['2']['total']
        self.__isAvailable =
        pass

    def reset(self, ):

        try:
            # 发送 POST 请求
            response0 = requests.post(f"http://{self.__main_address}/emeter/0/reset_totals", timeout=5)
            response0.raise_for_status()
            response1 = requests.post(f"http://{self.__main_address}/emeter/1/reset_totals", timeout=5)
            response1.raise_for_status()
            response2 = requests.post(f"http://{self.__main_address}/emeter/2/reset_totals", timeout=5)
            response2.raise_for_status()
            _info("复位成功! ")
        except requests.exceptions.RequestException as e:
            _info(f"复位失败: {e}")


