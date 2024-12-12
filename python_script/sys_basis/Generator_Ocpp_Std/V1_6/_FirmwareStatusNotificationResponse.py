
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class firmware_status_notification_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.FirmwareStatusNotification:
        """
        生成 FirmwareStatusNotificationResponse

        参数:
        - 

        返回值:
        - call_result.FirmwareStatusNotification
        """
        return call_result.FirmwareStatusNotification(
            
        )

