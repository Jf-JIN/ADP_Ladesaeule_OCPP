
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class status_notification_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.StatusNotification:
        """
        生成 StatusNotificationRequest

        参数:
        - 

        返回值:
        - call.StatusNotification
        """
        return call.StatusNotification(
            
        )

