#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Timer
import copy
import datetime

from python_script.sys_basis.GPIO._GPIO_Manager import GPIOManager
from sys_basis.XSignal import XSignal
from const.GPIO_Parameter import *
from tools.data_gene import *


if 0:
    from ._GPIO_Manager import GPIOManager


class DataCollector:
    def __init__(self, parent: GPIOManager, interval: int | float) -> None:
        self.__parent: GPIOManager = parent
        self.__intervall: int | float = interval
        self.__all_data: dict = {}
        self.__evse_data: dict = {}
        self.__shelly_data: dict = {}
        self.__timer: Timer = Timer(self.__intervall, self.__send_display_data)
        self.__charging_units_id_set: set = None
        self.__available_charge_units_id_set: set = None
        self.__signal_DC_data_display: XSignal = XSignal()
        self.__timer.start()

    @property
    def charging_units_id_set(self) -> set:
        """ 
        返回一个集合, 包含所有正在充电的充电单元的 id.
        """
        return self.__charging_units_id_set

    @property
    def available_charge_units_id_set(self) -> set:
        """ 
        返回一个集合, 包含所有可用的充电单元的 id.
        """
        return self.__available_charge_units_id_set

    @property
    def signal_DC_data_display(self) -> XSignal:
        """
        用于在数据收集器中发送数据的信号, 每隔 `self.__intervall` 秒发送一次.
        """
        return self.__signal_DC_data_display

    def set_evse_data(self, id: int, data: dict) -> None:
        """ 
        写入 EVSE 数据.
        """
        self.__evse_data[id] = data
        self.__check_id(id)
        self.__all_data[id]['evse'] = data

    def set_shelly_data(self, id: int, data: dict) -> None:
        """ 
        写入 Shelly 数据.
        """
        self.__shelly_data[id] = data
        self.__check_id(id)
        self.__all_data[id]['shelly'] = data

    def __add_charging_unit(self, id: int) -> None:
        """ 
        加入一个充电单元，该方法会在线程检查时被 set_CU_status 自动调用.
        """
        self.__charging_units_id_set.add(id)
        self.__available_charge_units_id_set.discard(id)

    def __remove_charging_unit(self, id: int) -> None:
        """ 
        移除一个充电单元，该方法会在线程检查时被 set_CU_status 自动调用.
        """
        self.__charging_units_id_set.discard(id)
        self.__available_charge_units_id_set.add(id)

    def set_CU_status(self, id: int, status: int) -> None:
        """ 
        写入充电单元状态.

        当状态为：
        - `VehicleState.READY`：充电单元就绪状态，可以充电
        - `VehicleState.EV_IS_PRESENT`：充电单元就绪状态，可以充电
        - `VehicleState.CHARGING`：充电单元正在充电，充电桩被占用
        - `VehicleState.CHARGING_WITH_VENTILATION`：充电单元正在充电，充电桩被占用
        - `VehicleState.FAILURE`：充电单元故障状态，充电桩被占用
        - `VehicleState.CRITICAL`：充电单元严重故障状态，充电桩被占用
        """
        self.__check_id(id)
        self.__all_data[id]['status'] = status
        if status in [VehicleState.READY]:
            # 充电单元就绪状态，可以充电
            self.__remove_charging_unit(id)
        elif status in [VehicleState.EV_IS_PRESENT, VehicleState.CHARGING, VehicleState.CHARGING_WITH_VENTILATION]:
            # 充电单元正在充电，充电桩被占用
            self.__add_charging_unit(id)
        elif status in [VehicleState.FAILURE, VehicleState.CRITICAL]:
            # 充电单元故障状态，充电桩被占用
            self.__add_charging_unit(id)

    def set_CU_current_charge_action(self, id: int, plan: dict) -> None:
        """ 
        设置充电单元当前充电计划.

        应输入的格式为字典，键值对为:
        - `startPeriod`：计划开始时间
        - `limit`：充电限制
        """
        self.__check_id(id)
        self.__all_data[id]['current_charge_action'] = plan

    def set_charge_start_time(self, id: int, time: str) -> None:
        """ 
        设置充电单元开始充电时间.

        应输入的格式为字符串，格式为"%Y-%m-%dT%H:%M:%SZ"
        """
        self.__check_id(id)
        self.__all_data[id]['start_time'] = time

    def set_CU_waiting_plan(self, id: int, plan: list) -> None:
        """
        设置充电单元等待充电计划.
        """
        self.__check_id(id)
        self.__all_data[id]['waiting_plan'] = plan

    def set_CU_finished_plan(self, id: int, plan: dict) -> None:
        plan = copy.deepcopy(plan)
        plan['finishedTime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.__check_id(id)
        self.__all_data[id]['finished_plan'] = plan

    def clear_CU_finished_plan(self, id: int) -> None:
        self.__check_id(id)
        self.__all_data[id]['finished_plan'] = []

    def set_CU_isLatched(self, id: int, flag: bool) -> None:
        self.__check_id(id)
        self.__all_data[id]['isLatched'] = flag

    def __check_id(self, id: int) -> None:
        """ 
        确保 id 一定在 __all_data 中存在.
        """
        if id not in self.__all_data:
            self.__all_data[id] = {}

    def __send_display_data(self) -> None:
        data: dict = {}
        self.__signal_DC_data_display.emit(data)
        self.__timer = Timer(self.__intervall, self.__send_display_data)
        self.__timer.start()
