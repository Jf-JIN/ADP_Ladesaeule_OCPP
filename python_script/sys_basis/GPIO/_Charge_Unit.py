import math
import threading
import time
from datetime import datetime
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from ._EVSE import Evse
from ._Shelly import Shelly
from tools.data_gene import DataGene


if 0:
    from sys_basis.GPIO import GPIOManager



class ChargeUnit:
    def __init__(self, parent, id, shelly_address):
        self.__parent: GPIOManager = parent
        self.__id:int = id
        self.__evse: Evse = Evse(id = id)
        self.__shelly: Shelly = Shelly(id = id,address= shelly_address)
        self.__status: int = -1
        self.__time_start:str = ''
        self.__time_depart:str = ''
        self.__info_title = 'ChargeUnit'
        #
        self.__charge_index: int = 0
        self.__current_start_time: datetime| None = None
        self.__unit: str = ''
        self.__current_periode:list = [0, 0]
        self.__request_periode:int = 4
        self.__target_energy: int = 0
        self.__current_limit:list = []
        #
        self.__timer: threading.Timer = threading.Timer(99, self.__charging)
        self.__finished_plan:list[dict] = []
        self.__waiting_plan:list[dict] = []
        self.__current_charge_action:dict = {}
        self.__isLatched:bool = False
        self.__signal_request_charge_plan_calibration:XSignal = XSignal()
        self.__signal_CU_info:XSignal = XSignal()
        self.__signal_charging_finished:XSignal = XSignal()

    @property
    def id(self):
        return self.__id

    @property
    def status(self)-> int:
        """
        可以反映是否在充电vehicle status
        """
        return self.__status

    @property
    def evse(self):
        return self.__evse

    @property
    def shelly(self):
        return self.__shelly

    @property
    def waiting_plan(self):
        return self.__waiting_plan

    @property
    def finished_plan(self):
        return self.__finished_plan

    @property
    def current_charge_action(self):
        return self.__current_charge_action

    @property
    def isLatched(self):
        return self.__isLatched

    @property
    def signal_request_charge_plan_calibration(self):
        return self.__signal_request_charge_plan_calibration

    @property
    def signal_CU_info(self):
        return self.__signal_CU_info

    @property
    def signal_charging_finished(self):
        return self.__signal_charging_finished

    def get_current_limit(self) -> list:
        return self.__evse.get_current_limit()

    def set_charge_plan(self, message:dict, target_energy: int | None = None, depart_time: str | None = None) -> bool:
        """
        处理堵塞的chargeing plan,处理矫正的charging plan
        """
        #判断计划的时效，将失效计划排除
        new_start_time = DataGene.str2time(message['chargingProfile']['chargingSchedule'][0]['startSchedule'])
        if not self.__current_start_time:
            self.__current_start_time = new_start_time

        else:
            if new_start_time < self.__current_start_time:
                #新计划的时间比正在执行的计划的时间早，当前计划更新，放弃计划
                self.__signal_CU_info.emit('充电计划时间早于当前计划，充电计划更新失败')
                return False
            else:
                self.__current_start_time = new_start_time


        #判断是不是给新车充电，如果是，重置shelly已充能量，evse开始自检,并设定target_energy和depart_time
        if target_energy and depart_time:
            self.__shelly.reset()
            self.__evse.start_self_check()
            self.__target_energy = target_energy
            self.__time_start =  message['chargingProfile']['chargingSchedule'][0]['startSchedule']
            self.__time_depart = depart_time
            self.__finished_plan = []


        #等待计划开始或修改滞后的计划
        current_timestamp = time.time()
        plan_timestamp = self.__current_start_time.timestamp()
        if current_timestamp < plan_timestamp:
            # 当前时间早于计划时间，需要等待
            lag_s = plan_timestamp - current_timestamp
            self.__timer = threading.Timer(lag_s, self.__charging,message)
            self.__timer.start()
            return True
        else:
            # 当前时间晚于计划时间，需要扣除迟滞时间
            lag_s = current_timestamp - plan_timestamp
            lag_m = math.ceil(lag_s / 60)
            message['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'] = self.__trim_charge_plan(lag_m = lag_m,plan_list = message['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'])
            if not message['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']:
                self.__signal_CU_info.emit('此计划滞后时间超过计划长度')
                return False
            else:
                self.__charging(message= message)
                return True



    def stop_charging(self, ):
        self.__evse.stop_charging()
        self.__status = VehicleState.CRITICAL


    def __start_charging(self, ):
        """主要是用于供按钮启动"""
        pass

    def __charging(self,message: dict):
        """实际运行的周期函数"""
        current_periode:list = self.__current_periode
        self.__set_unit(message)
        self.__waiting_plan = message
        if len(self.__waiting_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']) <= 0:
            self.__evse.stop_charging()
            self.__signal_charging_finished.emit()
            return
        self.__current_charge_action = self.__waiting_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'].pop(0)
        interval = (self.__waiting_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'][0]['startPeriod'] - self.__current_charge_action['startPeriod']) * 60
        #将换算的电流向下取整# TODO 具体的判断
        current = math.floor(self.__get_current_unit(self.__current_charge_action))
        self.__evse.set_current(current)
        current_periode[0] = self.__current_charge_action['startPeriod']  # current_periode += interval
        if current_periode[0] // self.__request_periode >= current_periode[1]:
            if current_periode[1] != 0:
                charged_emergy= self.__shelly.charged_energy()
                remaining_energy = self.__target_energy - charged_emergy
                self.__current_limit = self.__evse.get_current_limit()
                calibration_dict = {
                    'evMinCurrent': self.__current_limit[0],
                    'evMaxCurrent': self.__current_limit[1],
                    'evMaxVoltage': GPIOParams.MAX_VOLTAGE,
                    'energyAmount':remaining_energy,
                    'departureTime': self.__time_depart
                }

                self.signal_request_charge_plan_calibration.emit(calibration_dict)
            current_periode[1] = current_periode[0] // self.__request_periode
        threading.Timer(interval, self.__charging, [current_periode]).start()
        self.__finished_plan.append(self.__current_charge_action)



    def set_status(self, status):
        self.__status = status

    def __set_unit(self,data:dict):
        self.__unit = data['chargingProfile']['chargingSchedule'][0]['chargingRateUnit']

    def __get_current_unit(self,charging_plan: dict):
        if self.__unit == 'W':
            return charging_plan['limit'] / GPIOParams.MAX_VOLTAGE
        else:
            return charging_plan['limit']

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
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)

    def __handle_evse_errror(self, error_message):
        handle_dict= {
            EVSEErrorInfo.RCD_CHECK_ERROR: self.stop_charging,
            EVSEErrorInfo.RELAY_OFF: self.stop_charging,
            EVSEErrorInfo.VENT_REQUIRED_FAIL: self.stop_charging,
            EVSEErrorInfo.WAITING_FOR_PILOT_RELEASE: self.stop_charging,
            EVSEErrorInfo.DIODE_CHECK_FAIL: self.stop_charging,
            EVSEErrorInfo.RCD_CHECK_FAILED: self.stop_charging,
        }
        for error_item in error_message:
            if error_item in handle_dict:
                handle_dict[error_item]()


    def __trim_charge_plan(self,lag_m: int,plan_list: list):
        if lag_m > plan_list[-1]['startPeriod']:
            return []
        diff = lag_m - plan_list[0]['startPeriod']
        flag_new = True
        last_item = {}
        while len(plan_list) > 1:
            second_plan: dict = plan_list[1]
            first_plan: dict = plan_list[0]
            start_time = second_plan['startPeriod']
            if diff > 0:  # 当前时间大于执行时间，继续寻找
                last_item = plan_list.pop(0)
            else:
                if diff != 0:
                    current_time = first_plan['startPeriod'] - abs(diff)
                    last_item['startPeriod'] = current_time
                    if not flag_new:
                        plan_list.insert(0, last_item)
                break
            diff = lag_m - start_time
            flag_new = False
        return plan_list

