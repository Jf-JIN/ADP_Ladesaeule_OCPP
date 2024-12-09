
from ocpp.v201.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class change_availability_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.ChangeAvailability:
        """
        生成 ChangeAvailabilityResponse

        参数:
        - 

        返回值:
        - call_result.ChangeAvailability
        """
        return call_result.ChangeAvailability(
            
        )

