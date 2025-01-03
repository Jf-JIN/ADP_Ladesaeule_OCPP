
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_ev_charging_schedule_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(time_base, charging_schedule, evse_id, custom_data=None) -> call.NotifyEVChargingSchedule:
        """
        生成 NotifyEVChargingScheduleRequest

        参数:
            -

        返回值:
            - call.NotifyEVChargingSchedule
        """
        return call.NotifyEVChargingSchedule(
            time_base = time_base,
            charging_schedule = charging_schedule,
            evse_id = evse_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEVChargingSchedule:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyEVChargingSchedule
        """
        return call.NotifyEVChargingSchedule(
            time_base = dict_data['timeBase'],
            charging_schedule = dict_data['chargingSchedule'],
            evse_id = dict_data['evseId'],
            custom_data = dict_data.get('customData', None)
        )

