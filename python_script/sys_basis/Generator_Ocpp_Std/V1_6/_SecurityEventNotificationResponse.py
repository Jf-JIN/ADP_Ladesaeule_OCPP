from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenSecurityEventNotificationResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
    ) -> call_result.SecurityEventNotification:
        """
        Generate SecurityEventNotificationResponse

        - Args: 

        - Returns:
            - call_result.SecurityEventNotification
        """
        return call_result.SecurityEventNotification(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SecurityEventNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SecurityEventNotification
        """
        return call_result.SecurityEventNotification(
            
        )
