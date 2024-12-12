
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class change_availability(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.ChangeAvailability:
        """
        生成 ChangeAvailability

        参数:
        - 

        返回值:
        - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            
        )

