
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from ._Modbus_IO import ModbusIO
from ._EVSE_Self_Check import EVSESelfCheck
from DToolslib import EventSignal


_log = Log.EVSE


class Evse(object):
    signal_isInCharging: EventSignal = EventSignal(bool, async_exec=True)

    def __init__(self, id: int, doUseRCD: bool = False) -> None:
        self.__id: int = id
        self.__vehicle_status: int | None = None
        self.__evse_status_error: set = set()
        self.__doUseRCD: bool = doUseRCD
        self.__isEnableCharging: bool = True
        self.__isCharging = False
        self.__modbus: ModbusIO = ModbusIO(id)
        self.__signal_selftest_finished_result: XSignal = XSignal()
        self.__signal_evse_status_error: XSignal = XSignal()
        self.__signal_vehicle_status_failed_error = XSignal()
        self.__charging_timeout_counter = GPIOParams.CHARGING_STABLE_COUNTDOWN
        self.stop_charging()
        self.set_default_current(13)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def vehicle_state(self) -> int | None:
        return self.__vehicle_status

    @property
    def evse_status_error(self) -> set:
        return self.__evse_status_error

    @property
    def isEnableCharging(self) -> bool:
        return self.__isEnableCharging

    @property
    def isCharging(self) -> bool:
        return self.__isCharging

    @property
    def doUseRCD(self) -> bool:
        return self.__doUseRCD

    @property
    def signal_selftest_finished_result(self) -> XSignal:
        return self.__signal_selftest_finished_result

    @property
    def signal_evse_status_error(self) -> XSignal:
        return self.__signal_evse_status_error

    @property
    def signal_vehicle_status_failed_error(self) -> XSignal:
        return self.__signal_vehicle_status_failed_error

    def set_vehicle_state(self, state: int) -> None:
        self.__vehicle_status = state
        # _log.info(f'Vehicle state changed 1')
        if self.__isCharging:
            self.__detection_Charging_available(state)
        # _log.info(f'Vehicle state changed 2')
        if state == VehicleState.FAILURE:
            self.__isEnableCharging = False
            self.signal_vehicle_status_failed_error.emit(state)

    def set_evse_status_error(self, data: set) -> None:
        if (EVSEErrorInfo.WRITE_ERROR in data
                or EVSEErrorInfo.READ_ERROR in data):
            self.__isEnableCharging = False
            _log.warning(f'EVSE Error WRITE/READ ERROR: {data}')
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
            _log.warning(f'EVSE Error: {data}')
            self.__isEnableCharging = False
            self.__signal_evse_status_error.emit(self.__evse_status_error)
            return
        self.__isEnableCharging = True

    def set_current(self, value) -> bool:
        """
        给1000寄存器赋值,代表充电电流
        """
        self.__isCharging: bool = self.__set_current(value)
        return self.__isCharging

    def __set_current(self, value) -> bool:
        """
        给1000寄存器赋值,代表充电电流
        """
        if not self.__isEnableCharging:
            _log.error(f'EVSE {self.__id} is not enable charging')
            return False
        with self.__modbus as modbus:
            res_enable_charge = modbus.enable_charge(True)
            if not res_enable_charge:
                _log.error(f'EVSE {self.__id} enable charge failed')
                return False
            self.__isEnableCharging = True
            res_set_current: bool = modbus.set_current(value)
            if not res_set_current:
                _log.error(f'EVSE {self.__id} set current failed')
            return res_set_current
        return False

    def stop_charging(self) -> bool:
        """
        将1004寄存器的bit0: turn off charging now,置为1,表示立即停止充电
        """
        self.__isCharging: bool = not self.__stop_charging()  # 返回值表示是否成功停止充电, 与标志位相反, 如果停止充电成功,则将self.__isCharging置为False
        return self.__isCharging

    def __stop_charging(self) -> bool:
        """
        将1004寄存器的bit0: turn off charging now,置为1,表示立即停止充电
        """
        with self.__modbus as modbus:
            res_set_current = modbus.set_current(0)
            if not res_set_current:
                _log.error(f'EVSE {self.__id} set current 0 failed')
                return False
            res_enable_charge: bool = modbus.enable_charge(False)
            if not res_enable_charge:
                _log.error(f'EVSE {self.__id} stop charging failed')
            return res_enable_charge
        return False

    def set_default_current(self, value: int) -> bool:
        with self.__modbus as modbus:
            modbus.set_default_current(value)

    def start_self_check(self) -> None:
        selftest = EVSESelfCheck(self.__id, self.__doUseRCD)
        selftest.signal_self_test_error.connect(self.set_evse_status_error)
        selftest.signal_test_finished_result.connect(self.signal_selftest_finished_result.emit)
        selftest.signal_test_finished_result.connect(self.__handle_selftest_finished)
        selftest.start()

    def get_current_limit(self) -> list:
        """
        limit[0] = 最小电流
        limit[1] = 最大电流
        """
        limit = [-1, -1]
        with self.__modbus as modbus:
            _log.info(f'EVSE {self.__id} get current limit')
            limit[0] = modbus.read_current_min()
            limit[1] = modbus.read_current_max()
            _log.info(f'EVSE {self.__id} get current limit {limit}')
        return limit

    def __handle_selftest_finished(self, flag) -> None:
        if self.__doUseRCD:
            with self.__modbus as modbus:
                modbus.finish_selftest_and_RCD_test_procedure_with_RCD()
        else:
            with self.__modbus as modbus:
                modbus.finish_selftest_and_RCD_test_procedure()  # 不能使用with, isSelfChecking是True的状态, 不能进入with

    def __detection_Charging_available(self, status: int) -> bool:
        """
        检测充电桩在按计划充电中
        """
        _log.info(f'检测充电桩在按计划充电中{status} {self.__charging_timeout_counter}')
        if status == VehicleState.CHARGING:
            # _log.info(f'检测充电桩在按计划充电中 1')
            self.__charging_timeout_counter = GPIOParams.CHARGING_STABLE_COUNTDOWN
        else:
            # _log.info(f'检测充电桩在按计划充电中 2')
            if self.__charging_timeout_counter <= 0:
                # _log.info(f'检测充电桩在按计划充电中 3')
                self.signal_isInCharging.emit(False)
                self.__charging_timeout_counter = GPIOParams.CHARGING_STABLE_COUNTDOWN
                return False

            # _log.info(f'检测充电桩在按计划充电中 4')
            self.__charging_timeout_counter -= 1

        # _log.info(f'检测充电桩在按计划充电中 5')
        self.signal_isInCharging.emit(True)

        # _log.info(f'检测充电桩在按计划充电中 6')
        return True
