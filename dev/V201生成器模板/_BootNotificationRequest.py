
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class boot_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(charging_station, reason, custom_data=None) -> call.BootNotification:
        """
        生成 BootNotificationRequest

        参数:
            -

        返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charging_station = charging_station,
            reason = reason,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.BootNotification:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charging_station = dict_data['chargingStation'],
            reason = dict_data['reason'],
            custom_data = dict_data.get('customData', None)
        )

