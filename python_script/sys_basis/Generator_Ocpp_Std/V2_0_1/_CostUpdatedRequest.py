
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class cost_updated_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.CostUpdated:
        """
        生成 CostUpdatedRequest

        参数:
            - 

        返回值:
            - call.CostUpdated
        """
        return call.CostUpdated(
            
        )

