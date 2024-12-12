
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class set_charging_profile(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.SetChargingProfile:
        """
        生成 SetChargingProfile

        参数:
        - 

        返回值:
        - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            
        )

