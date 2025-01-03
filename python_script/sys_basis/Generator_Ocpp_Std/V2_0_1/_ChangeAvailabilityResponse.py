
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class change_availability_response(Base_OCPP_Struct_V2_0_1): 

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

