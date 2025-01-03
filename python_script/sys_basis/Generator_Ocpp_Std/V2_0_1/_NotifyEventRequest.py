
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_event_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.NotifyEvent:
        """
        生成 NotifyEventRequest

        参数:
            - 

        返回值:
            - call.NotifyEvent
        """
        return call.NotifyEvent(
            
        )

