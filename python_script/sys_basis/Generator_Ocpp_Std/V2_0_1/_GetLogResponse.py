
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_log_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetLog:
        """
        生成 GetLogResponse

        参数:
            - 

        返回值:
            - call_result.GetLog
        """
        return call_result.GetLog(
            
        )

