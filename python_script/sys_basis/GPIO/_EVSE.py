#!/usr/bin/python
# -*- coding: utf-8 -*-
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from _Modbus_IO import  ModbusIO
from _EVSE_Self_Check import EVSESelfCheck

class Evse(object):
    def __init__(self, id, doUseRCD):
        self.__id = id
        self.__vehicle_status = None
        #这个vehicle_status是哪里改?
        self.__evse_error = set()
        self.__doUseRCD = doUseRCD
        self.__isEnableCharging = None
        self.modbus = ModbusIO(id)

    @property
    def id(self):
        return self.__id

    @property
    def vehicle_state(self):
        return self.__vehicle_status

    @property
    def evse_error(self):
        return self.__evse_error

    @property
    def doUseRCD(self):
        return self.__doUseRCD

    def set_data(self, data):
        pass

    def set_evse_error(self, error_index: str):
        self.__evse_error.add(error_index)
        self.__isEnableCharging = False

    def set_current(self, value) -> bool :
        """
        给1000寄存器赋值,代表充电电流
        """
        with self.modbus as modbus:
            m = modbus.write(address=1000,value = value)
        return m

    def stop_charging(self, ):
        """
        将1004寄存器的bit0: turn off charging now,置为1,表示立即停止充电
        """
        with self.modbus as modbus:
            m = modbus.write(address=1004,value = REG1004.TURN_OFF_CHARGING_NOW)
        return m

    def start_self_check(self, ) -> bool :
        selftest = EVSESelfCheck(self.__id, self.__doUseRCD)
        selftest.signal_self_test_error.connect(self.__enable_charging)
        selftest.start()
        #这个要如何返回bool值？

    def get_current_limit(self, id) -> list:
        """
        limit[0] = 最小电流
        limit[1] = 最大电流
        """
        limit = [-1, -1]
        with self.modbus as modbus:
            limit[0] = modbus.read(address=2002)
            limit[1] = modbus.read(address=1003)
        return limit

    def __enable_charging(self, flag: bool) -> bool:
        self.__isEnableCharging = flag
        return self.__isEnableCharging

