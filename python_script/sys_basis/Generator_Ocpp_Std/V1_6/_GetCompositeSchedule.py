
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_composite_schedule(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.GetCompositeSchedule:
        """
        生成 GetCompositeSchedule

        参数:
            - 

        返回值:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            
        )

