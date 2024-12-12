
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_display_message_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SetDisplayMessage:
        """
        生成 SetDisplayMessageResponse

        参数:
        - 

        返回值:
        - call_result.SetDisplayMessage
        """
        return call_result.SetDisplayMessage(
            
        )

