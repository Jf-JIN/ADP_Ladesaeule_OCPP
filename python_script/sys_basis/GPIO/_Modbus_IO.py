#!/usr/bin/python
# -*- coding: utf-8 -*-

class ModbusIO:
    isSelfChecking = None

    def __init__(self):
        self.__id = None

    def read(self, address):
        pass

    def read_evse_status_and_fails(self, ):
        pass

    def write(self, address, value):
        pass

    def write_reg1004(self, bit, flag):
        pass

    def clear_turnOffChargingNow(self, ):
        pass

    def __init__(self, id):
        pass

    def __enter__(self, ):
        pass

    def __exit__(self, ):
        pass
