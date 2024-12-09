
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class get_composite_schedule_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetCompositeSchedule:
        """
        生成 GetCompositeScheduleResponse

        参数:
        - 

        返回值:
        - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            
        )

