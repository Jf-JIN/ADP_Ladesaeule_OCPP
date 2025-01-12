from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenDiagnosticsStatusNotificationResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        
    ) -> call_result.DiagnosticsStatusNotification:
        """
        Generate DiagnosticsStatusNotificationResponse

        - Args: 
            

        - Returns:
            - call_result.DiagnosticsStatusNotification
        """
        return call_result.DiagnosticsStatusNotification(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DiagnosticsStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.DiagnosticsStatusNotification
        """
        return call_result.DiagnosticsStatusNotification(
            
        )
