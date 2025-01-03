
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_variables_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetVariables:
        """
        生成 SetVariablesRequest

        参数:
            - 

        返回值:
            - call.SetVariables
        """
        return call.SetVariables(
            
        )

