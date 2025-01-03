
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class publish_firmware_status_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status, location=None, request_id=None, custom_data=None) -> call.PublishFirmwareStatusNotification:
        """
        生成 PublishFirmwareStatusNotificationRequest

        参数:
            -

        返回值:
            - call.PublishFirmwareStatusNotification
        """
        return call.PublishFirmwareStatusNotification(
            status = status,
            location = location,
            request_id = request_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.PublishFirmwareStatusNotification:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.PublishFirmwareStatusNotification
        """
        return call.PublishFirmwareStatusNotification(
            status = dict_data['status'],
            location = dict_data.get('location', None),
            request_id = dict_data.get('requestId', None),
            custom_data = dict_data.get('customData', None)
        )

