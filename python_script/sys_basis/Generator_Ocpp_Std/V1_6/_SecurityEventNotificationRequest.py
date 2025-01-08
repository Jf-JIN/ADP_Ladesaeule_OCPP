from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class security_event_notification_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        type: str,
        timestamp: str,
        tech_info: str | None = None
    ) -> call.SecurityEventNotification:
        """
        Generate SecurityEventNotificationRequest

        - Args: 
            - type(str): 
                - length limit: [1, 50]
            - timestamp(str): 
                - format: date-time
            - tech_info(str|None): 
                - length limit: [1, 255]

        - Returns:
            - call.SecurityEventNotification
        """
        return call.SecurityEventNotification(
            type = type,
            timestamp = timestamp,
            tech_info = tech_info
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SecurityEventNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SecurityEventNotification
        """
        return call.SecurityEventNotification(
            type = dict_data['type'],
            timestamp = dict_data['timestamp'],
            tech_info = dict_data.get('techInfo', None)
        )

