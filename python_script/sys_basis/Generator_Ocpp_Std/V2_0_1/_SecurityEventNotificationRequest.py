
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class security_event_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(type, timestamp, tech_info=None, custom_data=None) -> call.SecurityEventNotification:
        """
        生成 SecurityEventNotificationRequest

        参数:
            -

        返回值:
            - call.SecurityEventNotification
        """
        return call.SecurityEventNotification(
            type = type,
            timestamp = timestamp,
            tech_info = tech_info,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SecurityEventNotification:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SecurityEventNotification
        """
        return call.SecurityEventNotification(
            type = dict_data['type'],
            timestamp = dict_data['timestamp'],
            tech_info = dict_data.get('techInfo', None),
            custom_data = dict_data.get('customData', None)
        )

