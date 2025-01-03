
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class reset_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.Reset:
        """
        生成 ResetRequest

        参数:
            - 

        返回值:
            - call.Reset
        """
        return call.Reset(
            
        )

