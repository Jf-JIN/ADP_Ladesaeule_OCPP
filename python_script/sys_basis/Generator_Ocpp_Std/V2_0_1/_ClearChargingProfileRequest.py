
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class clear_charging_profile_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.ClearChargingProfile:
        """
        生成 ClearChargingProfileRequest

        参数:
        - 

        返回值:
        - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            
        )

