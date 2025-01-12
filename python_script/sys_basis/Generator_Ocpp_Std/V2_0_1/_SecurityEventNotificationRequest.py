from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenSecurityEventNotificationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        type: str,
        timestamp: str,
        tech_info: str | None = None,
        custom_data: dict | None = None
    ) -> call.SecurityEventNotification:
        """
        Generate SecurityEventNotificationRequest

        - Args: 
            - type(str): 
                - Type of the security event. This value should be taken from the Security events list. 
                - length limit: [1, 50]
            - timestamp(str): 
                - Date and time at which the event occurred. 
                - format: date-time
            - tech_info(str|None): 
                - Additional information about the occurred security event. 
                - length limit: [1, 255]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SecurityEventNotification
        """
        return call.SecurityEventNotification(
            type=type,
            timestamp=timestamp,
            tech_info=tech_info,
            custom_data=custom_data
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
            type=dict_data['type'],
            timestamp=dict_data['timestamp'],
            tech_info=dict_data.get('techInfo', None),
            custom_data=dict_data.get('customData', None)
        )
