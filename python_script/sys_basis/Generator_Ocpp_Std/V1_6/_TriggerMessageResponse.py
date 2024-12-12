
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class trigger_message_response(Base_OCPP_Struct_V1_6): 

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

