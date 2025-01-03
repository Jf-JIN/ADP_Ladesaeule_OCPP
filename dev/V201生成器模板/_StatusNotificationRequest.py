
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class status_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(timestamp, connector_status, evse_id, connector_id, custom_data=None) -> call.StatusNotification:
        """
        生成 StatusNotificationRequest

        参数:
            -

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            timestamp = timestamp,
            connector_status = connector_status,
            evse_id = evse_id,
            connector_id = connector_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StatusNotification:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            timestamp = dict_data['timestamp'],
            connector_status = dict_data['connectorStatus'],
            evse_id = dict_data['evseId'],
            connector_id = dict_data['connectorId'],
            custom_data = dict_data.get('customData', None)
        )

