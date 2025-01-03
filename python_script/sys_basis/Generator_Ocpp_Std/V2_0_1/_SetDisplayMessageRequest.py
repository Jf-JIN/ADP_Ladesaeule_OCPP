
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_display_message_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetDisplayMessage:
        """
        生成 SetDisplayMessageRequest

        参数:
            - 

        返回值:
            - call.SetDisplayMessage
        """
        return call.SetDisplayMessage(
            
        )

