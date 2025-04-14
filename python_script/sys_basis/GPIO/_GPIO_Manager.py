
import threading
from const.GPIO_Parameter import GPIOParams
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from ._Charge_Unit import *
from ._Thread_Polling_EVSE import PollingEVSE
from ._Thread_Polling_Shelly import PollingShelly
from ._Data_Collector import DataCollector
from ._Thread_Detection_Button import *
import atexit
import signal
# import RPi
from gpiozero import Button, LED
# from ._test_Module import Button, LED

_log = Log.GPIO


class GPIOManager:

    def __init__(self):
        self.__data_collector: DataCollector = DataCollector(self, GPIOParams.DATACOLLECTOR_DATA_INTERVAL, GPIOParams.DATACOLLECTOR_FIG_INTERVAL)
        atexit.register(self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.__charge_units_dict = {}
        self.__signal_GPIO_info: XSignal = XSignal()
        for item in GPIOParams.CHARGE_UNITS:
            charge_unit = ChargeUnit(self, *item)
            self.__charge_units_dict[item[0]] = charge_unit
            self.__data_collector.init_add_charge_units_id(item[0])
            charge_unit.signal_request_charge_plan_calibration.connect(self.__send_request_charge_plan_calibration)
            charge_unit.signal_hint_message.connect(self.__signal_GPIO_info.emit)

        self.__thread_polling_evse: PollingEVSE = PollingEVSE(self, self.__charge_units_dict, GPIOParams.POLLING_EVSE_INTERVAL)
        self.__thread_polling_shelly: PollingShelly = PollingShelly(self, self.__charge_units_dict, GPIOParams.POLLING_SHELLY_INTERVAL, GPIOParams.POLLING_SHELLY_TIMEOUT)
        self.__timer_send_requeset_calibration: threading.Timer = threading.Timer(
            GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
        self.__timer_send_requeset_calibration.name = 'GPIOManager.TimerSendRequestCalibration'

        self.__signal_request_charge_plan_calibration: XSignal = XSignal()
        self.__request_waiting_list: list = []
        self.__init_btn_event()

    def __init_btn_event(self):
        # RPi.GPIO.setmode(RPi.GPIO.BCM)
        # BTN_START = RaspPins.GPIO_17
        # BTN_STOP = RaspPins.GPIO_27
        # RPi.GPIO.setup(BTN_START, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        # RPi.GPIO.setup(BTN_STOP, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        # RPi.GPIO.add_event_detect(BTN_START, RPi.GPIO.FALLING, callback=self.__on_start_button_pressed, bouncetime=GPIOParams.BOUNCETIME)
        # RPi.GPIO.add_event_detect(BTN_STOP, RPi.GPIO.FALLING, callback=self.__on_stop_button_pressed, bouncetime=GPIOParams.BOUNCETIME)

        BTN_START = Button(RaspPins.BCM_PIN_20, pull_up=True)
        BTN_STOP = Button(RaspPins.BCM_PIN_21, pull_up=True)
        self.__button_led = LED(RaspPins.BCM_PIN_25)
        self.__thread_detection_button_start = DetectionButton('start', button=BTN_START)
        self.__thread_detection_button_stop = DetectionButton('start', button=BTN_STOP)
        self.__thread_detection_button_start.pressed.connect(self.__on_start_button_pressed)
        self.__thread_detection_button_stop.pressed.connect(self.__on_stop_button_pressed)
        self.__thread_detection_button_start.start()
        self.__thread_detection_button_stop.start()

    def stop(self):
        if self.__thread_polling_evse.is_alive():
            self.__thread_polling_evse.stop()
        if self.__thread_polling_shelly.is_alive():
            self.__thread_polling_shelly.stop()
        if self.__thread_detection_button_start.is_alive():
            self.__thread_detection_button_start.stop()
        if self.__thread_detection_button_stop.is_alive():
            self.__thread_detection_button_stop.stop()
        self.__data_collector.stop()
        self.__set_enable_button_LED(False)

    def __del__(self):
        self.stop()

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

    def set_charge_plan(self, data: dict, target_energy: int | None = None, depart_time: int | None = None, custom_data: dict | None = None, isManual: bool = False) -> bool:
        evse_id: int = data["evseId"]
        charge_unit: ChargeUnit = self.__charge_units_dict[evse_id]
        return charge_unit.set_charge_plan(data['chargingProfile'], target_energy, depart_time, custom_data, isManual)

    def get_current_limit(self, id: int) -> list | None:
        """
        获取允许的最小、最大电流值

        返回:
            list: [最小电流值(int), 最大电流值(int)]
            - 空列表表示无车辆插入
            None: Evse故障
        """
        if isinstance(id, str):
            id = int(id)
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        return charge_unit.get_current_limit()

    def get_voltage_max(self, id: int) -> int:
        """  获取允许的最大电压值 """
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        return charge_unit.get_voltage_max()

    def get_charge_unit(self, id: int) -> ChargeUnit:
        if id not in self.__charge_units_dict:
            _log.warning(f'未找到id为{id}的充电单元\nNo charging unit with ID {id} was not found')
        return self.__charge_units_dict[id]

    def stop_charging(self, id: int) -> None:
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        charge_unit.stop_charging()

    def clear_error(self, id: int) -> None:
        charge_unit: ChargeUnit = self.__charge_units_dict[id]
        charge_unit.clear_error()

    def listening_start(self) -> None:
        self.__thread_polling_evse.start()
        self.__thread_polling_shelly.start()
        self.__set_enable_button_LED(True)

    def __set_enable_button_LED(self, enable: bool) -> None:
        if enable:
            self.__button_led.on()
        else:
            self.__button_led.off()

    def __send_request_charge_plan_calibration(self, request_dict: dict) -> None:
        if self.__timer_send_requeset_calibration.is_alive():
            self.__request_waiting_list.append(request_dict)
        else:
            self.__signal_request_charge_plan_calibration.emit(request_dict)
            self.__timer_send_requeset_calibration = threading.Timer(GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
            self.__timer_send_requeset_calibration.name = 'GPIOManager.TimerSendRequestCalibration'
            self.__timer_send_requeset_calibration.start()

    def __execute_on_send_request_calibration_timer(self) -> None:
        self.__timer_send_requeset_calibration = threading.Timer(GPIOParams.REQUEST_INTERVAL, self.__execute_on_send_request_calibration_timer)
        self.__timer_send_requeset_calibration.name = 'GPIOManager.TimerSendRequestCalibration'
        if len(self.__request_waiting_list) > 0:
            self.__signal_request_charge_plan_calibration.emit(self.__request_waiting_list.pop(0))
            self.__timer_send_requeset_calibration.start()

    def __on_start_button_pressed(self, isPressed: bool):
        _log.warning('Button Start pressed')
        for unit in self.__charge_units_dict.values():
            unit: ChargeUnit
            if unit.hasChargePlan:
                enableDirectCharge: bool = False
            else:
                enableDirectCharge: bool = True
            unit.start_charging(enableDirectCharge)

    def __on_stop_button_pressed(self, isPressed: bool):
        _log.warning('Button Stop pressed')
        for unit in self.__charge_units_dict.values():
            unit: ChargeUnit
            unit.stop_charging()
