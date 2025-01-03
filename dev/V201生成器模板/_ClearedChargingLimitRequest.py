
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class cleared_charging_limit_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(charging_limit_source, evse_id=None, custom_data=None) -> call.ClearedChargingLimit:
        """
        生成 ClearedChargingLimitRequest

        参数:
            -

        返回值:
            - call.ClearedChargingLimit
        """
        return call.ClearedChargingLimit(
            charging_limit_source = charging_limit_source,
            evse_id = evse_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearedChargingLimit:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ClearedChargingLimit
        """
        return call.ClearedChargingLimit(
            charging_limit_source = dict_data['chargingLimitSource'],
            evse_id = dict_data.get('evseId', None),
            custom_data = dict_data.get('customData', None)
        )

