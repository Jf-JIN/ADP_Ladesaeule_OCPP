
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class clear_charging_profile(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.ClearChargingProfile:
        """
        生成 ClearChargingProfile

        参数:
            - 

        返回值:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            
        )

