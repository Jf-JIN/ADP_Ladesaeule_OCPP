
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_charging_limit_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.NotifyChargingLimit:
        """
        生成 NotifyChargingLimitResponse

        参数:
            - 

        返回值:
            - call_result.NotifyChargingLimit
        """
        return call_result.NotifyChargingLimit(
            
        )

