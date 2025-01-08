from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class log_status_notification_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | UploadLogStatus,
        request_id: int | None = None
    ) -> call.LogStatusNotification:
        """
        Generate LogStatusNotificationRequest

        - Args: 
            - status(str|UploadLogStatus): 
                - Enum: `BadMessage`, `Idle`, `NotSupportedOperation`, `PermissionDenied`, `Uploaded`, `UploadFailure`, `Uploading`
                - Or use EnumClass (Recommended): `UploadLogStatus`. e.g. `UploadLogStatus.bad_message`
            - request_id(int|None): 

        - Returns:
            - call.LogStatusNotification
        """
        return call.LogStatusNotification(
            status = status,
            request_id = request_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.LogStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.LogStatusNotification
        """
        return call.LogStatusNotification(
            status = dict_data['status'],
            request_id = dict_data.get('requestId', None)
        )

