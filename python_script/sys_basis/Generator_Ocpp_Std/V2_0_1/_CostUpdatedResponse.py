
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class cost_updated_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.CostUpdated:
        """
        生成 CostUpdatedResponse

        参数:
        - 

        返回值:
        - call_result.CostUpdated
        """
        return call_result.CostUpdated(
            
        )

