#!/usr/bin/python
# -*- coding: utf-8 -*-

class Shelly:
    def __init__(self):
        self.id = None
        self.main_address = None
        self.address_list = None
        self.sub_address_0 = None
        self.sub_address_1 = None
        self.sub_address_2 = None
        self.isAvailable = None
        self.charged_energy = None
        self.data = None
        self.data_ph0 = None
        self.data_ph1 = None
        self.data_ph2 = None
        self.signal_shelly_error_occured = None
        self.signal_current_no = None
        self.signal_current_overload = None
        self.__id = None
        self.__main_address = None
        self.__data = None
        self.__isAvailable = None
        self.__charged_energy = None
        self.__signal_current_no = None
        self.__signal_current_overload = None
        self.__signal_shelly_error_occured = None

    def set_data(self, data):
        pass

    def reset(self, ):
        pass

    def __init__(self, id, address):
        pass

    def Operation1(self, ):
        pass
