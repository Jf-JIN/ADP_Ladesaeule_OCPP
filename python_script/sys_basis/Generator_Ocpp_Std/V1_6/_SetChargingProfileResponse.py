
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class set_charging_profile_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.SetChargingProfile:
        """
        生成 SetChargingProfileResponse

        参数:
        - 

        返回值:
        - call_result.SetChargingProfile
        """
        return call_result.SetChargingProfile(
            
        )

