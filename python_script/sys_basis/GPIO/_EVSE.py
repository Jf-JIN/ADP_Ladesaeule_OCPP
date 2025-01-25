#!/usr/bin/python
# -*- coding: utf-8 -*-
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from _Modbus_IO import ModbusIO
from _EVSE_Self_Check import EVSESelfCheck

_error = Log.EVSE.error


class Evse(object):
    def __init__(self, id: int, doUseRCD: bool = False):
        self.__id: int = id
        self.__vehicle_status: int | None = None
        self.__evse_status_error: set = set()
        self.__doUseRCD: bool = doUseRCD
        self.__isEnableCharging: bool = True
        self.__modbus: ModbusIO = ModbusIO(id)
        self.__signal_selftest_finished: XSignal = XSignal()

    @property
    def id(self):
        return self.__id

    @property
    def vehicle_state(self):
        return self.__vehicle_status

    @property
    def evse_status_error(self):
        return self.__evse_status_error

    @property
    def isEnableCharging(self):
        return self.__isEnableCharging

    @property
    def doUseRCD(self):
        return self.__doUseRCD

    @property
    def signal_selftest_finished(self):
        return self.__signal_selftest_finished

    def set_vehicle_state(self, data: int):
        self.__vehicle_status = data

    def set_evse_status_error(self, data: set):
        if (EVSEErrorInfo.WRITE_ERROR in data
                or EVSEErrorInfo.READ_ERROR in data):
            self.__isEnableCharging = False
            return
        self.__evse_status_error = data
        if (
                EVSEErrorInfo.RCD_CHECK_FAILED in data
                or EVSEErrorInfo.RCD_CHECK_ERROR in data
                or EVSEErrorInfo.RELAY_OFF in data
                or EVSEErrorInfo.DIODE_CHECK_FAIL in data
                or EVSEErrorInfo.WAITING_FOR_PILOT_RELEASE in data
                or EVSEErrorInfo.VENT_REQUIRED_FAIL in data
        ):
            self.__isEnableCharging = False

    def set_current(self, value) -> bool:
        """
        给1000寄存器赋值,代表充电电流
        """
        if not self.__isEnableCharging:
            return False
        with self.__modbus as modbus:
            res0 = modbus.enable_charge(True)
            if not res0:
                _error(f'EVSE {self.__id} enable charge failed')
                return False
            self.__isEnableCharging = True
            m = modbus.set_current(value)
            if not m:
                _error(f'EVSE {self.__id} set current failed')
        return m

    def stop_charging(self) -> bool:
        """
        将1004寄存器的bit0: turn off charging now,置为1,表示立即停止充电
        """
        with self.__modbus as modbus:
            m = modbus.enable_charge(False)
            if not m:
                _error(f'EVSE {self.__id} stop charging failed')
        return m

    def start_self_check(self) -> None:
        selftest = EVSESelfCheck(self.__id, self.__doUseRCD)
        selftest.signal_self_test_error.connect(self.set_evse_status_error)
        selftest.signal_test_finished.connect(self.signal_selftest_finished.emit)
        selftest.start()

    def get_current_limit(self) -> list:
        """
        limit[0] = 最小电流
        limit[1] = 最大电流
        """
        limit = [-1, -1]
        with self.__modbus as modbus:
            limit[0] = modbus.read_current_min()
            limit[1] = modbus.read_current_max()
        return limit
