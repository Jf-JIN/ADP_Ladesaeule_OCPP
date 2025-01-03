
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_variables_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetVariables:
        """
        生成 GetVariablesRequest

        参数:
            - 

        返回值:
            - call.GetVariables
        """
        return call.GetVariables(
            
        )

