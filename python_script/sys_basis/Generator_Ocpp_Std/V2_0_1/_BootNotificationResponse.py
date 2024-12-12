
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class boot_notification_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.BootNotification:
        """
        生成 BootNotificationResponse

        参数:
        - 

        返回值:
        - call_result.BootNotification
        """
        return call_result.BootNotification(
            
        )

