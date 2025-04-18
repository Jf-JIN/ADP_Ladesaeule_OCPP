from __future__ import annotations
import threading
import sys
import copy
import time
from datetime import datetime
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from tools.data_gene import DataGene
from DToolslib import EventSignal
from ._EVSE import Evse
from ._Shelly import Shelly
from ._Latch_Motor import LatchMotor
from ._Manager_LED import *


if 0:
    from sys_basis.GPIO import GPIOManager
    from sys_basis.GPIO._Data_Collector import DataCollector

_log = Log.GPIO


class ChargeUnit:
    signal_hint_message = EventSignal(str, str)

    def __init__(self, parent: GPIOManager, id: int, shelly_address: str) -> None:
        self.__parent: GPIOManager = parent
        self.__id: int = id
        self.__evse: Evse = Evse(id=id)
        self.__shelly: Shelly = Shelly(self, id=id, address=shelly_address)
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__latch_motor: LatchMotor = LatchMotor(self, id=id)
        self.__start_time_str: str = ''
        """ 充电开始时间, 每次完整充电中只会被定义一次, 校正时不会更改 """
        self.__depart_time_str: str = ''
        """ 离开时间, 每次完整充电中只会被定义一次, 校正时不会更改 """
        self.__info_title = 'ChargeUnit'
        self.__custom_data: int = 0
        self.__isNoError: bool = True
        """ 用于记录是否有错误 """
        self.__isCharging: bool = False
        """ 用于标记是否在充电中, 供self.__execute_start_charging()判断使用, 若是, 则继续充电, 否则等待按钮或者网页指令 """
        self.__isLatched: bool = False
        """ 是否已经上锁 """
        self.__isTimeSynchronized = False
        """ 用于标记是否已经同步时间, 用于self.__charging() """
        self.__isEVSESelfTested: bool = False
        """ 用于标记是否已经进行过EVSE自检, 用于self.__prepare_charging() """
        self.__isFistTimeChanging: bool = True
        self.__isManual: bool = False
        """ 用于标记是否为手动输入 """
        self.__enableDirectCharge = False
        """ 用于标记是否为直接充电 """
        #
        self.__charge_index: int = 0
        """用于记录充电次数, 使用时间戳记录, 单位由self.__index_period_sec决定, 例如: self.__index_period_sec=3600, 则单位为小时"""
        self.__index_period_sec: int = GPIOParams.CALIBRATION_PERIOD
        """ 充电校正周期, 单位为秒 """
        self.__current_start_time_str: str = ''
        """ 当前充电计划表充电开始时间字符串, 校正时会被更改 """
        self.__current_start_datetime: datetime | None = None
        """ 当前充电计划表充电开始时间datetime, 校正时会被更改 """
        self.__value_unit: str = ''
        """ 充电计划表单位, 校正时会被更改 """
        self.__target_energy: int = 0
        """ 目标电量, 单位为Wh, 校正时不会更改 """
        self.__current_limit: list = []
        """ 当前限流, 单位为A, 调用方法 get_current_limit() 时更新 """
        self.__current_min: int = 0
        """ 当前限流最小值, 单位为A, 调用方法 get_current_limit() 时更新 """
        self.__current_max: int = sys.maxsize
        """ 当前限流最大值, 单位为A, 调用方法 get_current_limit() 时更新 """
        self.__voltage_max: int = GPIOParams.MAX_VOLTAGE
        #
        self.__timer: threading.Timer = threading.Timer(99, self.__charging)
        self.__timer.name = f'ChargeUnit<{self.__id}>'
        self.__lock_thread = threading.Timer(GPIOParams.LETCH_MOTOR_RUNTIME+0.5, self.__charging_initial)
        self.__lock_thread.name = f'ChargeUnit<{self.__id}>.chargingInitial_latchMotor'
        self.__evse_self_check_thread = threading.Timer(GPIOParams.SELF_CHECK_TIMEOUT+0.5, self.__charging_initial)
        self.__evse_self_check_thread.name = f'ChargeUnit<{self.__id}>.chargingInitial_evseSelfCheck'
        """ 充电计划定时器, 用于限制每个充电计划表项的执行时间, 确保不会超过计划表项的执行时间 """
        self.__finished_plan: list[dict] = []
        """ 已完成的充电计划项 """
        self.__waiting_plan: list[dict] = []
        """ 等待中的充电计划项 """
        self.__current_charge_action: dict = {}
        """ 当前正在执行的充电计划项 """

        self.__signal_request_charge_plan_calibration: XSignal = XSignal()
        self.__signal_CU_info: XSignal = XSignal()
        self.__signal_charging_finished: XSignal = XSignal()
        self.__signal_connections()

    def __signal_connections(self) -> None:
        self.evse.signal_vehicle_status_failed_error.connect(self.__handle_evse_error)
        self.evse.signal_evse_status_error.connect(self.__handle_evse_error)
        self.evse.signal_selftest_finished_result.connect(self.__set_isEVSESelfTested)
        self.evse.signal_isInCharging.connect(self.__check_and_stop_charging)
        self.shelly.signal_shelly_error_occurred.connect(self.__handle_shelly_error)
        self.shelly.signal_charged_energy.connect(self.__handle_shelly_charged_energy)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def parent_obj(self) -> GPIOManager:
        return self.__parent

    @property
    def vehicle_state(self) -> int:
        """
        可以反映是否在充电vehicle status
        """
        return self.evse.vehicle_state

    @property
    def isAvailabel(self) -> bool:
        """
        当前充电单元是否可用
        """
        if self.evse.vehicle_state is not None and self.evse.vehicle_state < 3 and self.__isNoError:
            return True
        else:
            return False

    @property
    def isCharging(self) -> bool:
        """
        当前充电单元是否正在充电
        """
        return self.__isCharging

    @property
    def evse(self) -> Evse:
        return self.__evse

    @property
    def shelly(self) -> Shelly:
        return self.__shelly

    @property
    def waiting_plan(self) -> list:
        return self.__waiting_plan

    @property
    def finished_plan(self) -> list:
        return self.__finished_plan

    @property
    def current_charge_action(self) -> dict:
        return self.__current_charge_action

    @property
    def isLatched(self) -> bool:
        return self.__isLatched

    @property
    def signal_request_charge_plan_calibration(self) -> XSignal:
        return self.__signal_request_charge_plan_calibration

    @property
    def signal_CU_info(self) -> XSignal:
        return self.__signal_CU_info

    @property
    def signal_charging_finished(self) -> XSignal:
        return self.__signal_charging_finished

    @property
    def hasChargePlan(self) -> bool:
        return bool(self.__waiting_plan)

    def get_current_limit(self) -> list | None:
        """
        返回:
            list: [最小电流值(int), 最大电流值(int)]
                - 空列表表示无车辆插入
            None: Evse故障
        """
        _log.info(f'开始获取当前电流限制范围，当前车辆状态为\nStart to obtain the current current limit range, the current vehicle status is:\t{self.__evse.vehicle_state}')
        if self.__evse.vehicle_state == VehicleState.READY:
            _log.warning('车辆未插入指定充电口，无法获取电流限制范围\nThe vehicle is not inserted in the specified charging port and the current restrictions cannot be obtained')
            self.__current_limit = [0, 0]
            self.__current_min = self.__current_limit[0]
            self.__current_max = self.__current_limit[1]
            return []
        elif VehicleState.EV_IS_PRESENT <= self.__evse.vehicle_state <= VehicleState.CHARGING_WITH_VENTILATION:
            _log.info('here')
            self.__current_limit = self.__evse.get_current_limit()
            self.__current_min = self.__current_limit[0]
            self.__current_max = self.__current_limit[1]
            _log.info(f'已获取到车辆充电电流限制范围\nGet the scope of the limitation of the vehicle charging current\n{self.__current_limit}')
            return self.__current_limit
        else:
            _log.error(f'The current vehicle status of ChargeUnit {self.id} is: {self.__evse.vehicle_state}. Unable to obtain current limit')
            self.__current_limit = [0, 0]
            self.__current_min = self.__current_limit[0]
            self.__current_max = self.__current_limit[1]
            return None

    def get_voltage_max(self) -> int:
        _log.info(f'已获取最大充电电压\nGet the maximum charging voltage\n{GPIOParams.MAX_VOLTAGE}')
        return GPIOParams.MAX_VOLTAGE

    def set_charge_plan(self, charging_profile: dict, target_energy: int | None = None, depart_time: str | None = None, custom_data: int | None = None, isManual: bool = False) -> bool:
        """
        处理堵塞的chargeing plan,处理矫正的charging plan

        charging_profile 字典结构
        'chargingProfile': {
            'id': 1,
            'stackLevel': 1,
            'chargingProfilePurpose': 'TxProfile',
            'chargingProfileKind': 'Absolute',
            'chargingSchedule': [
                {
                    'id': 1,
                    'chargingRateUnit': 'W',
                    'chargingSchedulePeriod': [
                        {'startPeriod': 0, 'limit': 9852},
                        ...
                    ],
                    'startSchedule': '2025-01-26T14:40:29Z'
                }
            ]
        }

        返回值:
        True: 成功
        False:
            - 充电列表长度为0
            - 新计划比当前计划早, 放弃执行
            - 新计划滞后时间超过新计划结束时间, 放弃执行
            - EVSE
        """
        _log.info(f'已收到充电计划，开始处理充电计划表\nThe charging plan has been received, and the charging plan form began to handle the charging plan')
        _log.debug(f'充电计划表\nCharging plan\n{charging_profile}')
        if not self.isAvailabel and not self.__isNoError:
            _log.warning('当前充电桩不可用,放弃执行充电\nThe current charging pile is not available, abandon the execution of the charging')
            return False
        charging_schedule_list = charging_profile['chargingSchedule']
        if len(charging_schedule_list) == 0:
            _log.warning('充电时间表清单为空,放弃执行充电\nThe charging timetable list is empty, give up the execution of the charging')
            return False
        # TODO:判断执行计划优先顺序
        exec_index = 0

        current_exec_dict = charging_schedule_list[exec_index]
        period_start_time: str = current_exec_dict['startSchedule']
        period_start_datetime: datetime = DataGene.str2time(period_start_time)

        if self.__isFistTimeChanging:
            # 首次充电计划, 参数重置
            _log.info(f'首次充电计划, 开始参数重置\nThe first charging plan, start parameter reset')
            self.__start_time_str = period_start_time
            self.__target_energy: int = target_energy
            self.__depart_time: str = depart_time
            self.__custom_data: int = custom_data
            self.__isManual: bool = isManual
            self.__finished_plan = []
            self.__current_charge_action = {}
            self.__data_collector.clear_CU_finished_plan(self.id)
        elif period_start_datetime < self.__current_start_datetime:
            # 非首次充电计划
            # 新计划的时间比正在执行的计划的时间早, 放弃执行新计划
            self.__signal_CU_info.emit('The charging plan is earlier than the current plan, and the update of the charging plan failed')
            _log.warning('非首次充电，充电计划比当前计划早，并且收费计划的更新失败\nNon -first charging, the charging plan is earlier than the current plan, and the update of the charging plan failed')
            return False

        # (非)首次充电计划
        # 新计划晚于或等于当前计划, 则正常执行计划
        self.__value_unit = current_exec_dict['chargingRateUnit']
        self.__current_start_time_str = period_start_time
        self.__current_start_datetime = period_start_datetime
        self.__depart_time_str = depart_time
        self.__waiting_plan = current_exec_dict['chargingSchedulePeriod']
        self.__isTimeSynchronized = False  # 强制对齐时间
        # 数据类重置
        _log.info('数据类重置更新\nData reset update')
        self.__data_collector.set_CU_waiting_plan(self.id, copy.deepcopy(self.__waiting_plan), self.__current_start_time_str)
        self.__data_collector.set_CU_charge_start_time(self.id, self.__start_time_str, self.__target_energy, self.__depart_time, self.__custom_data)
        self.__execute_start_charging()
        return True

    def start_charging(self, enableDirectCharge=False) -> bool:
        """
        主要是用于外部调用启动, 区别于接受充电计划表自动执行, 校正表时直接使用self.__execute_start_charging()

        - direct_charge: 用于直充
        """

        if (
            self.__evse.vehicle_state == VehicleState.EV_IS_PRESENT
            and self.__evse.evse_status_error == {EVSEErrorInfo.RELAY_ON}
            and self.__isNoError
            and self.__shelly.isAvailable
            and (enableDirectCharge or len(self.__waiting_plan) > 0)
        ):
            self.__isCharging = True
            self.__enableDirectCharge = enableDirectCharge
        elif (
                self.__evse.vehicle_state == VehicleState.EV_IS_PRESENT
                and self.__evse.evse_status_error == {EVSEErrorInfo.RELAY_ON}
                and self.__isNoError
                and self.__shelly.isAvailable
                and not len(self.__waiting_plan) > 0):
            _log.warning('当前没有充电计划表，无法启动充电\nAt present, there is no charging plan form, and the charging cannot be started')
            self.signal_hint_message.emit('当前没有充电计划表，无法启动充电\nAt present, there is no charging plan form, and the charging cannot be started', 'warning')
            return False
        else:
            _log.error(f"""\
EVSE State abnormal, Unable to start charging (correct value)
- vehicle_state (={VehicleState.EV_IS_PRESENT}): {self.__evse.vehicle_state}
- evse_status_error (ONLY 'Relay On'): {self.__evse.evse_status_error}
- Shelly isAvailable: {self.__shelly.isAvailable}
- isNoError (True): {self.__isNoError}
""")
            return False
        result: bool = self.__execute_start_charging()
        if not result:
            self.stop_charging()
        return result

    def __execute_start_charging(self) -> bool:
        """
        充电前期准备, 此部分主要是处理充电计划表, 将充电计划表与当前时间对齐
        """
        _log.info(f'开始充电前准备...\nPreparing for charging...\nenableDirectCharge: {self.__enableDirectCharge}')
        MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(True, apply_now=True, speed_s=0.1)
        if self.__enableDirectCharge:
            self.signal_hint_message.emit('开始直接充电\nStart direct charging', 'success')
            self.__charging_initial()
            return True
        if not self.__isCharging:
            # 如果当前没有充电计划, 则直接返回.
            # 保证新充电启动只会从外部触发, 内部函数不能启动.
            _log.warning(f'未点击开始，尚不执行充电\nThe Charge will not be executed without clicking start button')
            _log.warning(f'self.__isCharging is {self.__isCharging}, unable to start charging')
            return False
        _log.info('开始处理计划表\nStart processing the plan table')
        motor_runtime = GPIOParams.LETCH_MOTOR_RUNTIME if GPIOParams.LETCH_MOTOR_RUNTIME > 0 else 0
        evse_selfcheck_runtime = GPIOParams.SELF_CHECK_TIMEOUT if GPIOParams.SELF_CHECK_TIMEOUT >= 30 else 0
        current_timestamp: float = datetime.now().timestamp() + motor_runtime + evse_selfcheck_runtime
        plan_timestamp: float = self.__current_start_datetime.timestamp()
        if current_timestamp < plan_timestamp:
            # 当前时间早于计划时间, 需要等待
            lag_sec = plan_timestamp - current_timestamp
            _log.info(f'当前时间早于计划时间, 需要等待 {lag_sec} 秒\nThe current time is earlier than the planned time, you need to wait for {lag_sec} seconds')
            self.__timer = threading.Timer(lag_sec, self.__charging_initial)
            self.__timer.name = f'ChargeUnit<{self.__id}>.executeStartCharging'
            self.__timer.start()
        else:
            # 当前时间晚于计划时间, 需要扣除迟滞时间
            lag_sec: float = current_timestamp - plan_timestamp
            _log.info(f'当前时间晚于计划时间, 需要扣除迟滞时间 {lag_sec} 秒\nThe current time is later than the planned time, and the delay time {lag_sec} needs to be deducted')
            self.__waiting_plan = self.__trim_charge_plan(
                lag_sec=lag_sec,
                plan_list=self.__waiting_plan
            )
            if not self.__waiting_plan:
                _log.error('计划滞后时间超过计划结束时间\nPlan lag time exceeds the end of the plan')
                return False
            else:
                _log.info('已完成充电前的计划表准备\nPlanning table preparation before charging')
                self.__data_collector.set_CU_waiting_plan(self.id, copy.deepcopy(self.__waiting_plan), self.__current_start_time_str)
                self.__charging_initial()
        self.signal_hint_message.emit('充电前准备完成, 开始准备充电\nPreparation for charging is complete, start preparing for charging', 'success')
        return True

    def __charging_initial(self) -> None:
        """ 硬件初始化 """
        if self.__isFistTimeChanging:
            retry: int = 0
            while retry < 6:
                res = self.__shelly.reset()
                if res:
                    break
                else:
                    retry += 1
                    _log.warning(f'重置 Shelly 失败, 尝试次数: {retry}\nFailed to reset the Shelly, retry: {retry}')
                    time.sleep(0.5)
            if retry >= 6:
                self.stop_charging()
                _log.error('重置 Shelly 失败, 尝试次数: 6\n充电终止\nFailed to reset the charger, retry: 6\nCharging terminated')
                return
        if not self.__isLatched and self.__isFistTimeChanging and GPIOParams.LETCH_MOTOR_RUNTIME > 0:
            # 执行上锁操作, 执行条件: 1.当前未上锁 2. 首次执行充电 3.电机运行时间大于0
            self.__latch_motor.lock()
            _log.info('开始执行上锁\nStart locking')
            self.__lock_thread = threading.Timer(GPIOParams.LETCH_MOTOR_RUNTIME+0.5, self.__charging_initial)
            self.__lock_thread.name = f'ChargeUnit<{self.__id}>.chargingInitial_latchMotor'
            self.__lock_thread.start()
            return
        if not self.__isEVSESelfTested and self.__isFistTimeChanging and GPIOParams.SELF_CHECK_TIMEOUT >= 30:
            # 执行自检操作, 执行条件: 1.当前未自检 2. 首次执行充电 3.自检超时时间大于等于30s
            _log.info('开始执行evse自检\nStart EVSE self-check')
            self.__evse.start_self_check()
            self.__evse_self_check_thread = threading.Timer(GPIOParams.SELF_CHECK_TIMEOUT+0.5, self.__charging_initial)
            self.__evse_self_check_thread.name = f'ChargeUnit<{self.__id}>.chargingInitial_evseSelfCheck'
            self.__evse_self_check_thread.start()
            return
        _log.info('已完成充电前的上锁及EVSE自检\nThe lock and EVSE self -inspection before the charging')
        if self.__enableDirectCharge:
            self.__charging_direct()
        else:
            self.__charging()

    def __isExecutable(self) -> bool:
        """
        返回值:
            - True: 可以执行
            - False: 不能执行
                - 当前未在充电状态
                - 车辆状态为故障或严重故障
                - EVSE状态错误, 除了`EVSEErrorInfo.RELAY_ON`以外, 还有其他内容
                - 当前充电单元故障
                - 当前已无充电计划 / 充电计划全部完成
                - Shelly设备不可用
        """
        if (
            not self.__isCharging
            or not self.__shelly.isAvailable
            or self.__evse.vehicle_state == VehicleState.FAILURE
            or self.__evse.vehicle_state == VehicleState.CRITICAL
            or self.__evse.evse_status_error != {EVSEErrorInfo.RELAY_ON}
            or not self.__isNoError
            or (len(self.__waiting_plan) == 0 and not self.__enableDirectCharge)
        ):
            _log.error(f"""\
The charging unit is not executable (correct value)
- isCharging (True): {self.__isCharging}
- vehicle_state (<=4): {self.__evse.vehicle_state}
- evse_status_error (ONLY 'Relay On'): {self.__evse.evse_status_error}
- isNoError (True): {self.__isNoError}
- waiting_plan_list (>0): {len(self.__waiting_plan)}
- Shelly isAvailable(True): {self.__shelly.isAvailable}
""")
            MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(True, apply_now=True, speed_s=[0.1, 0.1, 0.1, 2])
            return False
        else:
            return True

    def __charging_direct(self) -> bool:
        """
        不做设置直接充电
        """
        self.get_current_limit()
        if self.__current_max > 0:
            self.__start_time_str = DataGene.time2str(datetime.now())
            _log.info('清空数据库对应数据\nClear database data corresponding to CU')
            self.__data_collector.clear_CU_finished_plan(self.id)
            self.__data_collector.clear_CU_waiting_plan(self.id)
            self.__data_collector.clear_CU_current_charge_action(self.id)
            self.__data_collector.set_CU_charge_start_time(self.id, self.__start_time_str, target_energy=-1, depart_time='-1', custom_data=None, enableDirectCharge=True)
            _log.info('设置电流, 开始充电\nSet current, start charging')
            self.__evse.set_current(self.__current_max)
            MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(True, apply_now=True)
            return True
        else:
            _log.info('最大电流为0,不充电\nThe maximum current is 0, no charging')
            self.signal_hint_message.emit(f'最大电流为0,不充电\nThe maximum current is 0, no charging', 'info')
            return False

    def __charging(self) -> bool:
        """
        实际运行的周期函数
        """
        def set_charging_current() -> bool:
            """
            设置电流, 开始充电
            """
            current = self.__convert_value_in_amps(self.__current_charge_action['limit'])
            return self.__evse.set_current(current)

        # 1. 检查是否可以执行, 不能则停止充电, 并发出信号
        _log.info('开始检查充电可行性\nStart checking the feasibility of charging')
        if not self.__isExecutable():
            self.stop_charging()
            self.__signal_charging_finished.emit()
            _log.warning('充电计划无法执行\nThe charging plan cannot be executed')
            return False
        # 2. 先存入上次的计划
        if self.__current_charge_action:
            self.__finished_plan.append(copy.copy(self.__current_charge_action))
            self.__data_collector.append_CU_finished_plan(self.id, copy.copy(self.__current_charge_action))
            _log.info(f'充电计划\t{self.__current_charge_action}\t已存入历史计划\nThe charging plan\t{self.__current_charge_action}\t has been saved into the historical plan')

        # 3. 取出充电动作, 计算单次充电时间
        self.__current_charge_action = self.__waiting_plan.pop(0)
        _log.info(f'开始充电，当前执行计划为\nStart charging, the current execution plan is\n{self.__current_charge_action}')
        _log.debug(f'剩余计划表\nRemaining planning table\n{self.__waiting_plan}')
        self.__data_collector.set_CU_waiting_plan(self.id, copy.deepcopy(self.__waiting_plan), self.__current_start_time_str)
        self.__data_collector.set_CU_current_charge_action(self.id, copy.copy(self.__current_charge_action))
        if len(self.__waiting_plan) != 0:
            charge_duration_sec: int | float = self.__waiting_plan[0]['startPeriod'] + DataGene.str2time(self.__current_start_time_str).timestamp() - datetime.now().timestamp()
        else:
            # charge_duration_sec: int | float = DataGene.str2time(self.__depart_time).timestamp() - self.__current_start_datetime.timestamp() - self.__current_charge_action['startPeriod']
            charge_duration_sec: int | float = (DataGene.str2time(self.__depart_time).timestamp() - self.__current_start_datetime.timestamp()) / \
                30 - self.__current_charge_action['startPeriod']  # [MODIFY] 该段代码仅用于测试，为了缩短时长而设置的，可通过修改 / 后的数字
        _log.info(f'当前充电动作时长为 {charge_duration_sec} 秒\nCurrent charge action duration is {charge_duration_sec} seconds')
        current_time: float = datetime.now().timestamp()
        current_index = current_time // self.__index_period_sec
        # _log.info(f'当前时间\t{current_time}\t当前充电周期戳\t{current_index}\t充电单位充电周期戳\t{self.__charge_index}\nCurrent timet{current_time}\tcurrent index{current_index}\tCU index{self.__charge_index}')
        # 4. 如果时间未同步, 则同步时间, 每个计划表的第一个充电周期都要进行时间同步/对齐
        if not self.__isTimeSynchronized:
            _log.info('时间未同步, 进行时间同步')
            if current_index != self.__charge_index:
                self.__charge_index = current_index
                _log.info('首次充电周期, 跳过校正, 更新充电周期戳\nThe first charging cycle, skips calibration, updates the charging cycle stamp')
            phase1_fill_time: int | float = self.__current_start_datetime.timestamp() + charge_duration_sec - current_time
            if phase1_fill_time < 0:
                phase1_fill_time = charge_duration_sec
            _log.info(f'时间同步, 首个充电动作时间: {phase1_fill_time} 秒')
            self.__isTimeSynchronized = True
            # 4.1 执行充电操作, 同时检查是否成功设置电流, 若否则停止充电
            result: bool = set_charging_current()
            if not result:
                self.stop_charging()
                self.__signal_charging_finished.emit()
                _log.error("Error setting charging current")
                return False
            MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(True, apply_now=True)
            self.__timer = threading.Timer(phase1_fill_time, self.__charging)
            self.__timer.name = f'ChargeUnit<{self.__id}>.charging'
            self.__timer.start()
            _log.info('充电时间同步完成, 开始等待至第一个周期开始\nThe charging time synchronization is completed, starting to wait for the first cycle')
            self.__isFistTimeChanging = False
            return True

        # 5. 跳过单充电计划中首个充电周期时的校正, 如果第一个周期就在校正触发时间上, 则跳过校正
        if current_index != self.__charge_index and self.__index_period_sec > 0 and not self.__isManual:
            _log.info('充电校正被触发，开始收集校正所需信息')
            self.__charge_index = current_index
            charged_emergy = self.__shelly.charged_energy
            remaining_energy = int(self.__target_energy - charged_emergy)
            current_limit_list = self.get_current_limit()
            if current_limit_list is None or len(current_limit_list) == 0:
                self.stop_charging()
                _log.error("获取电流限制错误\nError getting current limit")
                return False
            voltage_max = self.get_voltage_max()

            calibration_dict = {
                'evseId': self.__id,
                'evMinCurrent': self.__current_limit[0],
                'evMaxCurrent': self.__current_limit[1],
                'evMaxVoltage': voltage_max,
                'energyAmount': remaining_energy,
                'departureTime': self.__depart_time_str,
                'custom_data': self.__custom_data,
            }
            self.signal_request_charge_plan_calibration.emit(calibration_dict)
            _log.info('充电计划校正请求发送\nsending charging plan calibration request')

        # 6. 执行充电操作, 同时检查是否成功设置电流, 若否则停止充电
        result: bool = set_charging_current()
        if not result:
            self.stop_charging()
            _log.error("设置充电电流错误\nError setting charging current")
            return False
        MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(True, apply_now=True)
        self.__timer = threading.Timer(charge_duration_sec, self.__charging)
        self.__timer.name = f'ChargeUnit<{self.__id}>.charging'
        self.__timer.start()
        return True

    def stop_charging(self, error_code: str = '', sender: str = '') -> None:
        """
        停止充电
        添加结束动作
        关闭定时器
        发送充电结束信号
        解锁
        重置参数
        """
        _log.info(f'停止充电, 当前状态是否在充电: {self.__isCharging}\nStop charging, is charging: {self.__isCharging}')
        if not self.__isCharging:
            MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(False)
            MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable(True)
            if sender == 'web':
                self.signal_hint_message.emit(f'充电单元 <{self.id}> 未在充电, 无需停止\nCharge unit <{self.id}> is not charging, no need to stop', 'info')
            return
        _log.info('执行停止充电\nExecute stop charging')
        self.__evse.stop_charging()
        if self.__current_charge_action:
            self.__finished_plan.append(copy.copy(self.__current_charge_action))
            self.__data_collector.append_CU_finished_plan(self.id, copy.copy(self.__current_charge_action))
            self.__current_charge_action = None
        self.__waiting_plan.clear()
        if self.__lock_thread.is_alive():
            self.__lock_thread.cancel()
        if self.__evse_self_check_thread.is_alive():
            self.__evse_self_check_thread.cancel()
        if self.__timer.is_alive():
            self.__timer.cancel()
        self.__signal_charging_finished.emit()
        self.__latch_motor.unlock()
        # 进行初始化参数
        if error_code:
            self.__isNoError = False
            _log.error(f'充电单元[id:{self.id}]错误, 错误码: {error_code}\ncharge unit {self.id} has Errors, error code: {error_code}')
        self.__isCharging = False
        self.__isTimeSynchronized = False
        self.__isEVSESelfTested = False
        self.__isFistTimeChanging = True
        self.__enableDirectCharge = False
        self.__data_collector.stop_CU_charging(self.id)
        self.signal_hint_message.emit(f'充电单元 <{self.id}> 已停止充电\nCharge unit <{self.id}> has stopped charging', 'info')
        MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable_blink(False)
        MLED.getLed(LEDName.LED_SYSTEM_READY).set_enable(True)

    def clear_error(self) -> None:
        """ 慎用, 前端应做提示 """
        if self.__isNoError:
            _log.info('当前状态无错误, 无需清除\nThere is no error in the current state, no need to clear')
            self.signal_hint_message.emit('当前状态无错误, 无需清除\nThere is no error in the current state, no need to clear', 'info')
            return
        self.__isNoError = True
        _log.info('已清除错误\nError flag has been cleared')
        self.signal_hint_message.emit('已清除错误\nError flag has been cleared', 'success')

    def __check_and_stop_charging(self, isInCharging: bool) -> None:
        """ 是否应该停止充电 """
        # _log.info(f'检查是否应该停止充电 {isInCharging}')
        if not isInCharging:
            # _log.info(f'检查是否应该停止充电 1')
            if self.__isCharging:
                # _log.info(f'检查是否应该停止充电 2')
                self.signal_hint_message.emit('当前无车辆插入, 请检查并重新启动充电\nNo vehicle is inserted, please check and restart charging', 'info')
                self.stop_charging()

    def __convert_value_in_amps(self, charging_limit: int) -> int:
        """
        将充电限制值转换为安培值, 并限制在最小和最大电流之间
        """
        if self.__value_unit == 'W':
            charging_limit = charging_limit / GPIOParams.MAX_VOLTAGE
        round_amps = round(charging_limit)
        return max(min(round_amps, self.__current_max), self.__current_min)

    def __set_isEVSESelfTested(self, flag: bool) -> None:
        """ 设置是否已经进行过EVSE自检, 给信号使用的 """
        self.__isEVSESelfTested = flag
        if not flag:
            self.stop_charging('EVSE SelfTest Failed')
            return

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_CU_info, error_hint='send_signal_info', log=Log.OCPP.info,
                           doShowTitle=True, doPrintInfo=False, args=[*args])

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False,
                      doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        - 参数:
            - signal(XSignal): 信号对象
            - error_hint(str): 错误提示
            - log(Callable): 日志器动作
            - doShowTitle(bool): 是否显示标题
            - doPrintInfo(bool): 是否打印信息
            - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            if self.__info_title and doShowTitle:
                temp = f'< {self.__info_title} >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text: str = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)

    def __handle_evse_error(self, error_message: set | int) -> None:
        if isinstance(error_message, int):
            if error_message > 4:
                self.stop_charging(str(error_message))
                return
        handle_set: set = {
            EVSEErrorInfo.RCD_CHECK_ERROR,
            EVSEErrorInfo.RELAY_OFF,
            EVSEErrorInfo.VENT_REQUIRED_FAIL,
            EVSEErrorInfo.WAITING_FOR_PILOT_RELEASE,
            EVSEErrorInfo.DIODE_CHECK_FAIL,
            EVSEErrorInfo.RCD_CHECK_FAILED,
        }
        _log.info('error_message: ', error_message)
        for error_item in error_message:
            if error_item in handle_set:
                self.stop_charging(error_item)

    def __handle_shelly_error(self, error_flag: bool) -> None:
        if error_flag:  # True 存在错误
            self.stop_charging('shelly_error')

    def __handle_shelly_charged_energy(self, charged_energy: int | float) -> None:
        if charged_energy >= self.__target_energy and self.__target_energy > 0 and self.__isCharging:
            _log.info(f'已完成充电电量\nCharge finished, charged_energy\n{charged_energy}')
            self.signal_hint_message.emit(f'已完成充电, 充电电量{charged_energy}Wh\nCharge finished, charged_energy\n{charged_energy}Wh')
            self.stop_charging()

    def __trim_charge_plan(self, lag_sec: int | float, plan_list: list) -> list:
        if lag_sec > plan_list[-1]['startPeriod']:
            return []
        diff: int | float = lag_sec - plan_list[0]['startPeriod']
        flag_new = True
        last_item = {}
        while len(plan_list) > 1:
            second_plan: dict = plan_list[1]
            first_plan: dict = plan_list[0]
            start_time: int = second_plan['startPeriod']
            if diff > 0:  # 当前时间大于执行时间, 继续寻找
                last_item: dict = plan_list.pop(0)
            else:
                if diff != 0:
                    current_time: int | float = first_plan['startPeriod'] - abs(diff)
                    last_item['startPeriod'] = current_time
                    if not flag_new:
                        plan_list.insert(0, last_item)
                break
            diff: int | float = lag_sec - start_time
            flag_new = False
        return plan_list
