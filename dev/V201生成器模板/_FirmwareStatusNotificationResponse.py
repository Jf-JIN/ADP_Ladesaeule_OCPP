
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class firmware_status_notification_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data=None) -> call_result.FirmwareStatusNotification:
        """
        生成 FirmwareStatusNotificationResponse

        参数:
            -

        返回值:
            - call_result.FirmwareStatusNotification
        """
        return call_result.FirmwareStatusNotification(
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.FirmwareStatusNotification:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.FirmwareStatusNotification
        """
        return call_result.FirmwareStatusNotification(
            custom_data = dict_data.get('customData', None)
        )

