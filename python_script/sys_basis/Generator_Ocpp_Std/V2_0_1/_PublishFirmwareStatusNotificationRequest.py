
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class publish_firmware_status_notification_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.PublishFirmwareStatusNotification:
        """
        生成 PublishFirmwareStatusNotificationRequest

        参数:
        - 

        返回值:
        - call.PublishFirmwareStatusNotification
        """
        return call.PublishFirmwareStatusNotification(
            
        )

