
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class security_event_notification_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SecurityEventNotification:
        """
        生成 SecurityEventNotificationResponse

        参数:
        - 

        返回值:
        - call_result.SecurityEventNotification
        """
        return call_result.SecurityEventNotification(
            
        )

