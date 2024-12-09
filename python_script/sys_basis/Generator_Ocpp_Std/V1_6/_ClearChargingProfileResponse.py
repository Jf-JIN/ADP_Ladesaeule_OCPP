
from ocpp.v201.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class clear_charging_profile_response(Base_OCPP_Struct_V1_6): 

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

