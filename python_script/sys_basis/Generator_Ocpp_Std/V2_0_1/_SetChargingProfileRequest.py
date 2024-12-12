
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_charging_profile_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetChargingProfile:
        """
        生成 SetChargingProfileRequest

        参数:
        - 

        返回值:
        - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            
        )

