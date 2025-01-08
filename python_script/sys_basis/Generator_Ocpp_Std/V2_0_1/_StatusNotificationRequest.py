from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class status_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        timestamp: str,
        connector_status: str | ConnectorStatusType,
        evse_id: int,
        connector_id: int,
        custom_data: dict | None = None
    ) -> call.StatusNotification:
        """
        生成 StatusNotificationRequest

        - 参数: 
            - timestamp(str): 
                - The time for which the status is reported. If absent time of receipt of the message will be assumed. 
                - 格式: date-time
            - connector_status(str): 
                - This contains the current status of the Connector. 
                - 枚举值: `Available`, `Occupied`, `Reserved`, `Unavailable`, `Faulted`
                - 或使用枚举类(推荐)`ConnectorStatusType`. e.g. `ConnectorStatusType.available`
            - evse_id(int): 
                - The id of the EVSE to which the connector belongs for which the the status is reported. 
            - connector_id(int): 
                - The id of the connector within the EVSE for which the status is reported. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
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
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            timestamp = dict_data['timestamp'],
            connector_status = dict_data['connectorStatus'],
            evse_id = dict_data['evseId'],
            connector_id = dict_data['connectorId'],
            custom_data = dict_data.get('customData', None)
        )

