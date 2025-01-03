
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_ev_charging_needs_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(charging_needs, evse_id, max_schedule_tuples=None, custom_data=None) -> call.NotifyEVChargingNeeds:
        """
        生成 NotifyEVChargingNeedsRequest

        参数:
            -

        返回值:
            - call.NotifyEVChargingNeeds
        """
        return call.NotifyEVChargingNeeds(
            charging_needs = charging_needs,
            evse_id = evse_id,
            max_schedule_tuples = max_schedule_tuples,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEVChargingNeeds:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyEVChargingNeeds
        """
        return call.NotifyEVChargingNeeds(
            charging_needs = dict_data['chargingNeeds'],
            evse_id = dict_data['evseId'],
            max_schedule_tuples = dict_data.get('maxScheduleTuples', None),
            custom_data = dict_data.get('customData', None)
        )

