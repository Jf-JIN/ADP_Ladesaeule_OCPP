
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_display_messages_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetDisplayMessages:
        """
        生成 GetDisplayMessagesRequest

        参数:
            - 

        返回值:
            - call.GetDisplayMessages
        """
        return call.GetDisplayMessages(
            
        )

