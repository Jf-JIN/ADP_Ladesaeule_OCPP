
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_charging_limit_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data=None) -> call_result.NotifyChargingLimit:
        """
        生成 NotifyChargingLimitResponse

        参数:
            -

        返回值:
            - call_result.NotifyChargingLimit
        """
        return call_result.NotifyChargingLimit(
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.NotifyChargingLimit:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.NotifyChargingLimit
        """
        return call_result.NotifyChargingLimit(
            custom_data = dict_data.get('customData', None)
        )

