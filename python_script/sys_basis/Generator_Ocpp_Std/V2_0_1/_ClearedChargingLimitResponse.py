
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class cleared_charging_limit_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data=None) -> call_result.ClearedChargingLimit:
        """
        生成 ClearedChargingLimitResponse

        参数:
            -

        返回值:
            - call_result.ClearedChargingLimit
        """
        return call_result.ClearedChargingLimit(
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearedChargingLimit:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.ClearedChargingLimit
        """
        return call_result.ClearedChargingLimit(
            custom_data = dict_data.get('customData', None)
        )

