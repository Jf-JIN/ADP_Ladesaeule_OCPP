from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class boot_notification_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | RegistrationStatus,
        current_time: str,
        interval: int
    ) -> call_result.BootNotification:
        """
        Generate BootNotificationResponse

        - Args: 
            - status(str|RegistrationStatus): 
                - Enum: `Accepted`, `Pending`, `Rejected`
                - Or use EnumClass (Recommended): `RegistrationStatus`. e.g. `RegistrationStatus.accepted`
            - current_time(str): 
                - format: date-time
            - interval(int): 

        - Returns:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            status = status,
            current_time = current_time,
            interval = interval
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.BootNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            status = dict_data['status'],
            current_time = dict_data['currentTime'],
            interval = dict_data['interval']
        )

