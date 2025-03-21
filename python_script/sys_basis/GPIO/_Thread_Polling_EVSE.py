from __future__ import annotations
from threading import Thread
from ._Modbus_IO import ModbusIO
from const.GPIO_Parameter import *
from const.Const_Parameter import *
import time


if 0:
    from ._GPIO_Manager import GPIOManager
    from ._Charge_Unit import ChargeUnit
    from ._Data_Collector import DataCollector
    from ._EVSE import Evse

_log = Log.EVSE


class PollingEVSE(Thread):
    def __init__(self, parent: GPIOManager, charge_unit_dict: dict, intervall: int | float) -> None:
        super().__init__()
        self.__parent: GPIOManager = parent
        self.__evse_list: list = []
        for item in charge_unit_dict.values():
            item: ChargeUnit
            self.__evse_list.append(item.evse)
        self.__evse_quantity: int = len(self.__evse_list)
        self.__interval: int | float = intervall
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__isRunning: bool = True
        self.__current_index: int = 0

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def run(self) -> None:
        while self.__isRunning:
            evse: Evse = self.__evse_list[self.__current_index]
            evse_id: int = evse.id
            evse_data = {}
            with ModbusIO(id=evse_id) as io:
                vehicle_state: int | None = io.read_vehicle_status()  # timeout 由 Modbus 决定
                if vehicle_state is not None:
                    evse_data['vehicle_state'] = vehicle_state
                    evse.set_vehicle_state(vehicle_state)

                evse_error: None | set = io.read_evse_status_fails()
                if evse_error is not None:
                    evse_data['evse_error'] = evse_error
                    evse.set_evse_status_error(evse_error)
                else:
                    _log.error(f'EVSE {evse_id} read error')

                if len(evse_data):
                    self.__data_collector.set_evse_data(evse_id, evse_data)
            self.__current_index = (self.__current_index + 1) % self.__evse_quantity
            time.sleep(self.__interval)

    def stop(self) -> None:
        self.__isRunning = False
        self.join()
