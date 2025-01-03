
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class firmware_status_notification_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate() -> call_result.FirmwareStatusNotification:
        """
        生成 FirmwareStatusNotificationResponse

        参数:
            -

        返回值:
            - call_result.FirmwareStatusNotification
        """
        return call_result.FirmwareStatusNotification(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.FirmwareStatusNotification:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.FirmwareStatusNotification
        """
        return call_result.FirmwareStatusNotification(
            
        )

