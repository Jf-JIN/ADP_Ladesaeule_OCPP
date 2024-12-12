
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class reset_response(Base_OCPP_Struct_V1_6): 

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

