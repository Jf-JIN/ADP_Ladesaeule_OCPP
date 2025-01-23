#!/usr/bin/python
# -*- coding: utf-8 -*-

class ChargeUnit:
    def __init__(self):
        self.id = None
        self.status = None
        self.evse = None
        self.shelly = None
        self.isCharging = None
        self.waiting_plan = None
        self.finished_plan = None
        self.current_charge_action = None
        self.isLachted = None
        self.signal_request_charge_plan_calibration = None
        self.signal_finished_charge_plan = None
        self.signal_CU_info = None
        self.signal_charging_finished = None
        self.__parent = None
        self.__id = None
        self.__evse = None
        self.__shelly = None
        self.__status = None
        self.__isCharging = None
        self.__time_start = None
        self.__time_depart = None
        self.__time_last_item = None
        self.__charge_index = None
        self.__timer = None
        self.__finished_plan = None
        self.__waiting_plan = None
        self.__current_charge_action = None
        self.__isLachted = None
        self.__signal_request_charge_plan_calibration:XSignal = None
        self.__signal_finished_charge_plan = None
        self.__signal_CU_info = None
        self.__signal_charging_finished = None

    def get_current_limit(self, id):
        pass

    def get_max_current(self, ):
        pass

    def set_charge_plan(self, message, target_energy, depart_time):
        pass

    def stop_charging(self, ):
        pass

    def __init__(self, parent, id, shelly_address):
        pass

    def __start_charging(self, ):
        """主要是用于供按钮启动"""
        pass

    def __charging(self, ):
        """实际运行的周期函数"""
        pass

    def __send_signal_info(self, ):
        pass

    def __handle_evse_errror(self, error_message):
        pass
