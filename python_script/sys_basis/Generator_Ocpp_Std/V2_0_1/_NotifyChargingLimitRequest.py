
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_charging_limit_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(charging_limit, charging_schedule=None, evse_id=None, custom_data=None) -> call.NotifyChargingLimit:
        """
        生成 NotifyChargingLimitRequest

        参数:
            -

        返回值:
            - call.NotifyChargingLimit
        """
        return call.NotifyChargingLimit(
            charging_limit = charging_limit,
            charging_schedule = charging_schedule,
            evse_id = evse_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyChargingLimit:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyChargingLimit
        """
        return call.NotifyChargingLimit(
            charging_limit = dict_data['chargingLimit'],
            charging_schedule = dict_data.get('chargingSchedule', None),
            evse_id = dict_data.get('evseId', None),
            custom_data = dict_data.get('customData', None)
        )

