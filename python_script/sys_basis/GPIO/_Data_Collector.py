#!/usr/bin/python
# -*- coding: utf-8 -*-

class DataCollector:
    def __init__(self):
        self.charging_units_id_set = None
        self.available_charge_units_id_set = None
        self.signal_DC_data_display = None
        self.__all_data = None
        self.__interval = None
        self.__timer = None
        self.__charging_units_id_set = None
        self.__available_charge_units_id_set = None
        self.__signal_DC_data_display = None

    def set_evse_data(self, id, data):
        pass

    def set_shelly_data(self, id, data):
        pass

    def add_charging_unit(self, ):
        pass

    def remove_charging_unit(self, ):
        pass

    def set_CU_status(self, id, status):
        pass

    def set_CU_current_charge_action(self, id, plan):
        pass

    def set_CU_waiting_plan(self, id, plan):
        pass

    def set_CU_finished_plan(self, id, plan):
        pass

    def set_CU_isLatched(self, id, flag):
        pass

    def __init__(self, parent, interval):
        pass

    def __send_display_data(self, ):
        pass
