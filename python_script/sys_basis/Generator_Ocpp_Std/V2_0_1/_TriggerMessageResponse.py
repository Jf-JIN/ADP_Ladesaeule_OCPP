
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class trigger_message_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.TriggerMessage:
        """
        生成 TriggerMessageResponse

        参数:
        - 

        返回值:
        - call_result.TriggerMessage
        """
        return call_result.TriggerMessage(
            
        )

