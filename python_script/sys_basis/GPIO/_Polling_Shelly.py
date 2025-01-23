#!/usr/bin/python
# -*- coding: utf-8 -*-

class PollingShelly:
    def __init__(self):
        self.isRunning = None
        self.__parent = None
        self.__shelly_list = None
        self.__interval = None
        self.__timeout = None
        self.__data_collector = None
        self.__isRunning = None
        self.__current_index = None

    def run(self, ):
        pass

    def stop(self, ):
        pass

    def __init__(self, parent, charge_unit_list, intervall, timeout):
        pass
