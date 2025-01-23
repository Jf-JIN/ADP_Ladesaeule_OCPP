#!/usr/bin/python
# -*- coding: utf-8 -*-

class Evse:
    def __init__(self):
        self.id = None
        self.isVehicleConnected = None
        self.vehicle_state = None
        self.evse_error = None
        self.doUseRCD = None
        self.__id = None
        self.__isVehicleConnected = None
        self.__isVehicleConnected = None
        self.__vehicle_status = None
        self.__evse_error = None
        self.__doUseRCD = None
        self.__isEnableCharging = None

    def set_register(self, address, data):
        pass

    def set_data(self, data):
        pass

    def set_evse_error(self, error_index):
        pass

    def set_current(self, value):
        pass

    def stop_charging(self, ):
        pass

    def start_self_check(self, ):
        pass

    def get_current_limit(self, id):
        pass

    def __init__(self, id, doUseRCD):
        pass

    def __enable_charging(self, flag):
        pass

    def get_max_voltage(self, ):
        pass
