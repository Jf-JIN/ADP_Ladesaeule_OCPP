
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_display_messages_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetDisplayMessages:
        """
        生成 GetDisplayMessagesResponse

        参数:
        - 

        返回值:
        - call_result.GetDisplayMessages
        """
        return call_result.GetDisplayMessages(
            
        )

