
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class boot_notification_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(current_time, interval, status) -> call_result.BootNotification:
        """
        生成 BootNotificationResponse

        参数:
            -

        返回值:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            current_time = current_time,
            interval = interval,
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.BootNotification:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            current_time = dict_data['currentTime'],
            interval = dict_data['interval'],
            status = dict_data['status']
        )

