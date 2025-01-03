
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class firmware_status_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status, request_id=None, custom_data=None) -> call.FirmwareStatusNotification:
        """
        生成 FirmwareStatusNotificationRequest

        参数:
            -

        返回值:
            - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            status = status,
            request_id = request_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.FirmwareStatusNotification:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            status = dict_data['status'],
            request_id = dict_data.get('requestId', None),
            custom_data = dict_data.get('customData', None)
        )

