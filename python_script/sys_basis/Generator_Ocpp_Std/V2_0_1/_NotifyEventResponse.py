
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_event_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.NotifyEvent:
        """
        生成 NotifyEventResponse

        参数:
        - 

        返回值:
        - call_result.NotifyEvent
        """
        return call_result.NotifyEvent(
            
        )

