
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class clear_charging_profile_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.ClearChargingProfile:
        """
        生成 ClearChargingProfileResponse

        参数:
            - 

        返回值:
            - call_result.ClearChargingProfile
        """
        return call_result.ClearChargingProfile(
            
        )

