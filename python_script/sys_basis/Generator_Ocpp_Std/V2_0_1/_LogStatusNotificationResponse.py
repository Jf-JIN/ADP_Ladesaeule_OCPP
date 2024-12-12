
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class log_status_notification_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.LogStatusNotification:
        """
        生成 LogStatusNotificationResponse

        参数:
        - 

        返回值:
        - call_result.LogStatusNotification
        """
        return call_result.LogStatusNotification(
            
        )

