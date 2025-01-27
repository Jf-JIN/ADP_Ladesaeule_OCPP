
import threading
from const.GPIO_Parameter import GPIOParams
from sys_basis.XSignal import XSignal
from _Charge_Unit import ChargeUnit
from _Thread_Polling_EVSE import PollingEVSE
from _Thread_Polling_Shelly import PollingShelly
from _Data_Collector import DataCollector


class GPIOManager:
    def __init__(self):
        self.__charge_units_dict = {}
        for item in GPIOParams.CHARGE_UNITS:
            charge_unit = ChargeUnit(self, *item)
            self.__charge_units_dict[item[0]] = charge_unit
            charge_unit.signal_request_charge_plan_calibration.connect(self.__send_request_charge_plan_calibration)

        self.__charge_unit_init_param_list = None
        self.__thread_polling_evse: PollingEVSE = PollingEVSE(self, self.__charge_units_dict, GPIOParams.POLLING_EVSE_INTERVAL)
        self.__thread_polling_shelly: PollingShelly = PollingShelly(self, self.__charge_units_dict, GPIOParams.POLLING_SHELLY_INTERVAL)
        self.__data_collector: DataCollector = DataCollector(self, self.__charge_units_dict, GPIOParams.DATACOLLECTOR_DATA_INTERVAL, GPIOParams.DATACOLLECTOR_FIG_INTERVAL)
        self.__timer_send_requeset_calibration: threading.Timer = threading.Timer(GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
        self.__signal_GPIO_info: XSignal = XSignal()
        self.__signal_request_charge_plan_calibration: XSignal = XSignal()
        self.__request_waiting_list: list = []
        self.__thread_polling_evse.start()
        self.__thread_polling_shelly.start()

    @property
    def data_collector(self) -> DataCollector:
        return self.__data_collector

    @property
    def signal_GPIO_info(self) -> XSignal:
        return self.__signal_GPIO_info

    @property
    def signal_request_charge_plan_calibration(self) -> XSignal:
        return self.__signal_request_charge_plan_calibration

    @property
    def charge_units_dict(self) -> dict:
        return self.__charge_units_dict

    def set_charge_plan(self, data: dict, target_energy: int | None = None, depart_time: int | None = None) -> bool:
        evse_id: int = data["evseId"]
        charge_unit: ChargeUnit = self.__charge_units_dict[evse_id]
        return charge_unit.set_charge_plan(data, target_energy, depart_time)

    def get_current_limit(self, id: int) -> list | None:
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        return charge_unit.get_current_limit()

    def stop_charging(self, id: int) -> None:
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        charge_unit.stop_charging()

    def clear_error(self, id: int) -> None:
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        charge_unit.clear_error()

    def __send_request_charge_plan_calibration(self, request_dict: dict) -> None:
        if self.__timer_send_requeset_calibration.is_alive():
            self.__request_waiting_list.append(request_dict)
        else:
            self.__signal_request_charge_plan_calibration.emit(request_dict)
            self.__timer_send_requeset_calibration = threading.Timer(GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
            self.__timer_send_requeset_calibration.start()

    def __execute_on_send_request_calibration_timer(self) -> None:
        self.__timer_send_requeset_calibration = threading.Timer(GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
        if len(self.__request_waiting_list) > 0:
            self.__signal_request_charge_plan_calibration.emit(self.__request_waiting_list.pop(0))
            self.__timer_send_requeset_calibration.start()
