#!/usr/bin/python
# -*- coding: utf-8 -*-

class GPIOManager:
    def __init__(self):
        self.data_collector = None
        self.signal_GPIO_info = None
        self.signal_GPIO_display_data = None
        self.__charge_units_dict = None
        self.__charge_unit_init_param_list = None
        self.__thread_polling_evse = None
        self.__thread_polling_shelly = None
        self.__data_collector = None
        self.__timer_send_requeset_calibration = None
        self.__signal_GPIO_info = None
        self.__signal_GPIO_display_data = None

    def set_charge_plan(self, message, target_energy, depart_time):
        pass

    def get_current_limit(self, id):
        pass

    def stop_charging(self, id):
        pass

    def __init__(self, ):
        pass

    def __send_request_charge_plan_calibration(self, message):
        pass

    def __execute_on_send_request_calibration_timer(self, ):
        pass
