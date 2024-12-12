
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_variables_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SetVariables:
        """
        生成 SetVariablesResponse

        参数:
        - 

        返回值:
        - call_result.SetVariables
        """
        return call_result.SetVariables(
            
        )

