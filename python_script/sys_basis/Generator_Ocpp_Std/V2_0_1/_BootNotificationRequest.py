
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class boot_notification_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.BootNotification:
        """
        生成 BootNotificationRequest

        参数:
        - 

        返回值:
        - call.BootNotification
        """
        return call.BootNotification(
            
        )

