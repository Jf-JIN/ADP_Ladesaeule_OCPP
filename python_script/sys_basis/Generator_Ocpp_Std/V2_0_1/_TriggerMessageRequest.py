
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class trigger_message_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.TriggerMessage:
        """
        生成 TriggerMessageRequest

        参数:
        - 

        返回值:
        - call.TriggerMessage
        """
        return call.TriggerMessage(
            
        )

