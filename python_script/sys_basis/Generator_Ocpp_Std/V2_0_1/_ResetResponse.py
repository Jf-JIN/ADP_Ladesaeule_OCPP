
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class reset_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.Reset:
        """
        生成 ResetResponse

        参数:
        - 

        返回值:
        - call_result.Reset
        """
        return call_result.Reset(
            
        )

