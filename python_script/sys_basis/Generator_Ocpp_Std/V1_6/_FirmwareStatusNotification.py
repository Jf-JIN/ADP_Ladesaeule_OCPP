
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class firmware_status_notification(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.FirmwareStatusNotification:
        """
        生成 FirmwareStatusNotification

        参数:
        - 

        返回值:
        - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            
        )

