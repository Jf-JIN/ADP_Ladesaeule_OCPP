from __future__ import annotations
from threading import Timer
import copy
import datetime

from sys_basis.XSignal import XSignal
from const.GPIO_Parameter import *
from const.Const_Parameter import *

from tools.data_gene import *
from DToolslib import EventSignal


if 0:
    from ._GPIO_Manager import GPIOManager

_log = Log.GPIO


class DataCollector:
    """

    - 参数:
        - gpio_manager(GPIOManager): GPIOManager对象
        - interval_send_data(int|float): 发送数据数据的间隔时间, 单位: 秒, 默认: 1秒
        - interval_send_fig(int|float): 发送图像数据的间隔时间, 单位: 秒, 默认: 30秒

    - 属性:
        - charging_units_id_set(set): 充电单元ID集合
        - available_charge_units_id_set(set): 可用的充电单元ID集合
        - parent_object(GPIOManager): 父对象

    - 信号:
        - signal_DC_data_display(XSignal): DC数据显示信号
        - signal_DC_figure_display(XSignal): DC图像显示信号

    - 方法:
        - 硬件数据
            - set_evse_data(id, data): 设置EVSE数据, 线程使用
            - set_shelly_data(id, data): 设置Shelly数据, 线程使用
        - 充电单元数据
            - set_CU_charge_start_time(id, start_time, target_energy, depart_time): 设置充电单元开始充电时间
            - set_CU_current_charge_action(id, plan): 设置充电单元当前充电动作
            - set_CU_waiting_plan(id, plan, period_start_time): 设置充电单元等待计划
            - append_CU_finished_plan(id, plan): 添加充电单元完成计划
            - clear_CU_finished_plan(id): 清除充电单元完成计划
            - set_CU_isLatched(id, flag): 设置充电单元是否锁存

    - 数据总格式示例(self.__all_data): `请转到定义处查看`
    {\
        1: {\
            'evse': {\
                'vehicle_state': VehicleState.EVSE_IS_PRESENT,\
                'evse_error': EVSEErrorInfo.RELAY_ON,
                <register_address>: {
                    "function_code": <int>,
                    "registers": <list>,
                    "status": <int>, 
                    "isError": <bool>,
                    "exception_code": <int>,
                    "dev_id": <>,
                    "transaction_id": <int>,
                    "bits": <list>,
                    "address": <int>,
                }
            },
            'shelly': {
                0: {
                    'power': 0,
                    'pf': 0,
                    'current': 0,
                    'voltage': 0,
                    'is_valid': true,
                    'total': 0,
                },
                1: {
                    'power': 0,
                    'pf': 0,
                    'current': 0,
                    'voltage': 0,
                    'is_valid': true,
                    'total': 0,
                },
                2: {
                    'power': 0,
                    'pf': 0,
                    'current': 0,
                    'voltage': 0,
                    'is_valid': true,
                    'total': 0,
                },
                'charged_energy': 0,
                'is_valid': true,
            },
            'status': VehicleState.EV_IS_PRESENT,
            'waiting_plan': [
                {'startPeriod': 35, 'limit': 9855},
                {'startPeriod': 50, 'limit': 8863},
                ...
            ],
            'current_charge_action': {
                'startPeriod': 20,
                'limit': 8523,
                'startTime': '2025-01-26T15:00:02Z',
                'finishedTime': '2025-01-26T15:23:30Z',
                'chargedEnergy': 3600,
                },
            'finished_plan': [
                {'startPeriod': 0, 'limit': 9852, 'startTime':'2025-01-26T14:40:29Z','finishedTime': '2025-01-26T14:45:21Z', 'chargedEnergy':780,},
                {'startPeriod': 5, 'limit': 9724, 'startTime':'2025-01-26T14:40:29Z','finishedTime': '2025-01-26T15:00:02Z', 'chargedEnergy':3500,},
                {'startPeriod': 0, 'limit': 9852, 'startTime':'2025-01-26T15:00:02Z','finishedTime': '2025-01-26T15:05:02Z', 'chargedEnergy':4108,},
                {'startPeriod': 5, 'limit': 9724, 'startTime':'2025-01-26T15:00:02Z','finishedTime': '2025-01-26T15:20:02Z', 'chargedEnergy':6958,},
            ],
            # 'finished_plan_figure_base64': <base64_string>,
            'start_time': '2025-01-26T14:40:29Z', # 此开始时间指的是整个充电过程, 校正的计划表中的开始一时间不会记录
            'period_start_time': '2025-01-26T15:00:02Z', # 此开始时间指一个充电表的开始时间, 校正的计划表中的开始时间会被记录
            'depart_time': '2025-01-30T13:39:00Z',
            'charged_time': '00:43:01,'
            'target_energy': 700000,
            'isLatched': True,
            'custom_data': {'mode': 0, 'vendorId'='1234'},
            'enableDirectCharge': False,
            'direct_charge_energy_list':[]
        },
        2:{
            ...
        },
        ...
    }
    """

    __instance__ = None
    signal_DC_watching_data_display = EventSignal(dict)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(
        self,
        parent: GPIOManager,
        interval_send_data: int | float = 1,
        interval_send_fig: int | float = 30,
        interval_send_watching_data: int | float = 1,
    ) -> None:
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True
        self.__parent: GPIOManager = parent
        self.__interval_send_data: int | float = interval_send_data
        self.__interval_send_fig: int | float = interval_send_fig
        self.__interval_send_watching_data: int | float = interval_send_watching_data
        self.__all_data: dict = {}
        self.__evse_data: dict = {}
        self.__shelly_data: dict = {}
        self.__timer_data: Timer = Timer(self.__interval_send_data, self.__send_display_data)
        self.__timer_data.name = 'DataCollector.data'
        self.__timer_figure: Timer = Timer(self.__interval_send_fig, self.__send_figure_data)
        self.__timer_figure.name = 'DataCollector.figure'
        self.__timer_watching: Timer = Timer(self.__interval_send_watching_data, self.__send_watchting_data)
        self.__timer_watching.name = 'DataCollector.watching'
        self.__charging_units_id_set: set = set()
        self.__available_charge_units_id_set: set = set()
        self.__signal_DC_data_display: XSignal = XSignal()
        self.__signal_DC_figure_display: XSignal = XSignal()
        self.__timer_data.start()
        self.__timer_figure.start()
        self.__timer_watching.start()
        self.__isRunning = True
        """ 表示是否存在充电桩在充电中/准备充电 """

    def stop(self) -> None:
        self.__timer_data.cancel()
        self.__timer_figure.cancel()
        self.__timer_watching.cancel()
        self.__isRunning = False

    def __str__(self) -> str:
        return f"""Data Collector:\
< all_data >: {str(self.__all_data)}

< evse >: {str(self.__evse_data)}

< shelly >: {str(self.__shelly_data)}
"""

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
        用于在数据收集器中发送数据的信号, 每隔 `self.__interval_send_data` 秒发送一次.
        """
        return self.__signal_DC_data_display

    @property
    def signal_DC_figure_display(self) -> XSignal:
        """
        用于在数据收集器中发送图片数据的信号, 每当数据更新时就发送一次.
        """
        return self.__signal_DC_figure_display

    @property
    def parent_obj(self) -> GPIOManager:
        return self.__parent

    def init_add_charge_units_id(self, id: int) -> None:
        """
        加入一个充电单元, 该方法会在线程检查时被 set_CU_status 自动调用.
        """
        self.__available_charge_units_id_set.add(id)

    def set_evse_data(self, id: int, data: dict) -> None:
        """
        写入 EVSE 数据.
        """
        self.__evse_data[id] = data
        self.__check_id(id)
        self.__all_data[id]['evse'] = data
        self.__set_CU_status(id, data['vehicle_state'])

    def set_shelly_data(self, id: int, data: dict) -> None:
        """
        写入 Shelly 数据.
        """
        self.__shelly_data[id] = data
        self.__check_id(id)
        self.__all_data[id]['shelly'] = data
        if not self.__all_data[id].get('current_charge_action', None):
            self.__all_data[id]['current_charge_action'] = {}
        self.__all_data[id]['current_charge_action']['chargedEnergy'] = data.get('charged_energy', 0)

    def set_CU_current_charge_action(self, id: int, plan: dict) -> None:
        """
        设置充电单元当前充电计划.

        应输入的格式为字典, 键值对为:
        - `startPeriod`: 计划开始时间
        - `limit`: 充电限制
        """
        self.__check_id(id)
        plan = copy.deepcopy(plan)
        plan['startTime'] = self.__all_data[id]['period_start_time']
        plan['finishedTime'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        plan['chargedEnergy'] = self.__all_data[id]['shelly']['charged_energy']
        self.__all_data[id]['current_charge_action'] = plan
        self.__isRunning = True

    def set_CU_charge_start_time(self, id: int, start_time: str, target_energy: int, depart_time: str, custom_data: int | None = None, enableDirectCharge=False) -> None:
        """
        设置充电单元开始充电时间.

        应输入的格式为字符串, 格式为"%Y-%m-%dT%H:%M:%SZ"
        """
        self.__check_id(id)
        self.__all_data[id]['start_time'] = start_time
        self.__all_data[id]['target_energy'] = target_energy
        self.__all_data[id]['depart_time'] = depart_time
        self.__all_data[id]['custom_data'] = custom_data
        self.__all_data[id]['enableDirectCharge'] = enableDirectCharge
        self.__all_data[id]['direct_charge_energy_list'] = []
        self.__all_data[id]['isCharging'] = True

    def set_CU_waiting_plan(self, id: int, plan: list, period_start_time: str | None = None) -> None:
        """
        设置充电单元等待的充电计划.
        """
        self.__check_id(id)
        self.__all_data[id]['waiting_plan'] = plan
        if period_start_time:
            self.__all_data[id]['period_start_time'] = period_start_time
        elif 'period_start_time' not in self.__all_data[id] and 'start_time' in self.__all_data[id]:
            self.__all_data[id]['period_start_time'] = self.__all_data[id]['start_time']
        # 如果开始时间大于计划开始时间, 则将开始时间设置为计划开始时间
        if ('period_start_time' in self.__all_data and 'start_time' in self.__all_data[id]
            and (
            DataGene.str2time(self.__all_data[id]['start_time'])
            > DataGene.str2time(self.__all_data[id]['period_start_time'])
        )
        ):
            self.__all_data[id]['period_start_time'] = self.__all_data[id]['start_time']

    def get_CU_evse_data(self, id: int) -> dict:
        self.__check_id(id)
        return self.__all_data[id]['evse']

    def get_CU_shelly_data(self, id: int) -> dict:
        self.__check_id(id)
        return self.__all_data[id]['shelly']

    def clear_CU_waiting_plan(self, id: int) -> None:
        self.__check_id(id)
        self.__all_data[id]['waiting_plan'] = []

    def append_CU_finished_plan(self, id: int, plan: dict) -> None:
        """
        追加充电单元已完成的充电计划.
        """
        plan = copy.deepcopy(plan)
        plan['startTime'] = self.__all_data[id]['period_start_time']
        plan['finishedTime'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        plan['chargedEnergy'] = self.__all_data[id]['shelly']['charged_energy']
        self.__check_id(id)
        if 'finished_plan' not in self.__all_data[id]:
            self.__all_data[id]['finished_plan'] = []
        self.__all_data[id]['finished_plan'].append(plan)
        # 计算已充电时间
        diff_seconds = (DataGene.str2time(plan['finishedTime']) - DataGene.str2time(plan['startTime'])).total_seconds()
        hours, minites_seconds = divmod(diff_seconds, 3600)
        minutes, seconds = divmod(minites_seconds, 60)
        charged_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.__all_data[id]['charged_time'] = charged_time_str
        self.__all_data[id]['current_charge_action'] = {}
        self.__send_figure_data()

    def clear_CU_finished_plan(self, id: int) -> None:
        """
        清空充电单元已完成的充电计划.
        """
        self.__check_id(id)
        self.__all_data[id]['finished_plan'] = []

    def clear_CU_current_charge_action(self, id: int) -> None:
        self.__check_id(id)
        self.__all_data[id]['current_charge_action'] = {}

    def stop_CU_charging(self, id: int) -> None:
        """
        停止充电单元的充电.
        """
        self.__check_id(id)
        self.__all_data[id]['isCharging'] = False

    def set_CU_isLatched(self, id: int, flag: bool) -> None:
        """
        设置充电单元是否上锁.
        """
        self.__check_id(id)
        self.__all_data[id]['isLatched'] = flag

    def __add_charging_unit(self, id: int) -> None:
        """
        加入一个充电单元, 该方法会在线程检查时被 set_CU_status 自动调用.
        """
        self.__charging_units_id_set.add(id)
        self.__available_charge_units_id_set.discard(id)
        self.__isRunning = True

    def __remove_charging_unit(self, id: int) -> None:
        """
        移除一个充电单元, 该方法会在线程检查时被 set_CU_status 自动调用.
        """
        self.__charging_units_id_set.discard(id)
        self.__available_charge_units_id_set.add(id)
        if len(self.__charging_units_id_set) == 0:
            self.__isRunning = False

    def __set_CU_status(self, id: int, status: int) -> None:
        """
        写入充电单元状态.

        当状态为:
        - `VehicleState.READY`: 充电单元就绪状态, 可以充电
        - `VehicleState.EV_IS_PRESENT`: 充电单元就绪状态, 可以充电
        - `VehicleState.CHARGING`: 充电单元正在充电, 充电桩被占用
        - `VehicleState.CHARGING_WITH_VENTILATION`: 充电单元正在充电, 充电桩被占用
        - `VehicleState.FAILURE`: 充电单元故障状态, 充电桩被占用
        - `VehicleState.CRITICAL`: 充电单元严重故障状态, 充电桩被占用
        """
        self.__check_id(id)
        self.__all_data[id]['status'] = status
        if status in [VehicleState.READY, VehicleState.EV_IS_PRESENT]:
            # 充电单元就绪状态, 可以充电
            self.__remove_charging_unit(id)
            # self.clear_CU_finished_plan(id) # [Attention] 暂时注释掉, 如果想在充电结束后不保留图像的话, 可以取消注释
        elif status in [VehicleState.CHARGING, VehicleState.CHARGING_WITH_VENTILATION]:
            # 充电单元正在充电, 充电桩被占用
            self.__add_charging_unit(id)
        elif status in [VehicleState.FAILURE, VehicleState.CRITICAL]:
            # 充电单元故障状态, 充电桩被占用
            self.__add_charging_unit(id)

    def __check_id(self, id: int) -> None:
        """
        确保 id 一定在 __all_data 中存在.
        """
        if id not in self.__all_data:
            self.__all_data[id] = {
                'waiting_plan': [],
                'current_charge_action': {},
                'finished_plan': [],
                'depart_time': '',
                'charged_time': '',
                'target_energy': 0,
                'custom_data': {},
                'enableDirectCharge': False,
            }

    def __send_watchting_data(self) -> None:
        """
        发送监控的数据
        """
        for cu_data in self.__all_data.values():
            # _log.info(f'cu_data: {cu_data}')
            evse_data: dict = copy.deepcopy(cu_data.get('evse', {}))
            evse_data.pop('vehicle_state') if 'vehicle_state' in evse_data else None
            evse_data.pop('evse_error') if 'evse_error' in evse_data else None
            shelly_data: dict = cu_data.get('shelly', {})
            sehlly_0_data: dict = shelly_data.get(0, {})
            sehlly_1_data: dict = shelly_data.get(1, {})
            sehlly_2_data: dict = shelly_data.get(2, {})
            shelly_charged_energy = shelly_data.get('charged_energy', 0)
            shelly_is_valid: bool = shelly_data.get('is_valid', False)
            data: dict = {
                'current_time': datetime.now().strftime('%Y-%m-%d | %H:%M:%S.%f')[:-3],
                'evse': evse_data,
                'shelly': {
                    "0": sehlly_0_data,
                    "1": sehlly_1_data,
                    "2": sehlly_2_data,
                    'charged_energy': shelly_charged_energy,
                    'is_valid': shelly_is_valid,
                },
            }
            # _log.info(data)
            self.signal_DC_watching_data_display.emit(data)
        self.__timer_watching = Timer(self.__interval_send_watching_data, self.__send_watchting_data)
        self.__timer_watching.name = 'DataCollector.watching'
        self.__timer_watching.start()

    def __send_display_data(self) -> None:
        """
        发送文字数据
        """
        data: dict = {

        }
        if data:
            self.__signal_DC_data_display.emit(data)
        self.__timer_data = Timer(self.__interval_send_data, self.__send_display_data)
        self.__timer_data.name = 'DataCollector.data'
        self.__timer_data.start()

    def __send_figure_data(self) -> None:
        """
        发送图片数据
        """
        data: dict = {}
        for cu_id in self.__all_data:
            self.__check_id(cu_id)
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            if self.__all_data[cu_id]['enableDirectCharge']:
                if 'direct_charge_energy_list' not in self.__all_data[cu_id] or not isinstance(self.__all_data[cu_id]['direct_charge_energy_list'], list):
                    self.__all_data[cu_id]['direct_charge_energy_list'] = []
                img_list: list = self.__all_data[cu_id]['direct_charge_energy_list']
                if self.__all_data[cu_id]['isCharging']:
                    if len(img_list) == 0:
                        last_finished_time: str = self.__all_data[cu_id]['start_time']
                        charged_energy = 0
                    else:
                        last_finished_time = img_list[-1]['finishedTime']
                        charged_energy = self.__all_data[cu_id]['current_charge_action'].get('chargedEnergy', 0)
                    temp: dict = {
                        'finishedTime': current_time,
                        'chargedEnergy': charged_energy,
                        'limit': 0,
                        'startPeriod': (DataGene.str2time(last_finished_time) - DataGene.str2time(self.__all_data[cu_id]['start_time'])).total_seconds(),
                        'startTime': self.__all_data[cu_id]['start_time'],
                    }
                    img_list.append(temp)
                fig: str = DataGene.plan2figure(img_list)
                # self.__all_data[cu_id]['finished_plan_figure_base64'] = fig
            else:
                finished_plan: list = self.__all_data[cu_id].get('finished_plan', [])
                current_charge_action: dict = self.__all_data[cu_id].get('current_charge_action', {})
                if current_charge_action and 'startTime' in current_charge_action:
                    current_charge_action['finishedTime'] = current_time
                    img_list = finished_plan + [current_charge_action]
                else:
                    img_list = finished_plan
                fig: str = DataGene.plan2figure(img_list)
                # self.__all_data[cu_id]['finished_plan_figure_base64'] = fig
            # if fig:
            data['cp_fig'] = fig  # TODO 可以添加ID
        # 此处可以适配id，当前不支持多个充电单元图像，当存在多个单元时，只会发送最后一个图像。如有需要多个图像显示此处可以进行修改，并同时修改Javascript代码
        if data:
            self.__signal_DC_figure_display.emit(data)
        if self.__timer_figure.is_alive():
            self.__timer_figure.cancel()
        self.__timer_figure = Timer(self.__interval_send_fig, self.__send_figure_data)
        self.__timer_figure.name = 'DataCollector.figure'
        self.__timer_figure.start()
