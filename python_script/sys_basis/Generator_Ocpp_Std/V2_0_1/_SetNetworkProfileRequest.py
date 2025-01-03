
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_network_profile_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetNetworkProfile:
        """
        生成 SetNetworkProfileRequest

        参数:
            - 

        返回值:
            - call.SetNetworkProfile
        """
        return call.SetNetworkProfile(
            
        )

