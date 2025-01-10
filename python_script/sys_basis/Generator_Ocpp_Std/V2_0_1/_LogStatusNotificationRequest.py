from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenLogStatusNotificationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | UploadLogStatusType,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.LogStatusNotification:
        """
        Generate LogStatusNotificationRequest

        - Args: 
            - status(str): 
                - This contains the status of the log upload. 
                - Enum: `BadMessage`, `Idle`, `NotSupportedOperation`, `PermissionDenied`, `Uploaded`, `UploadFailure`, `Uploading`, `AcceptedCanceled`
                - Or use EnumClass (Recommended): `UploadLogStatusType`. e.g. `UploadLogStatusType.bad_message`
            - request_id(int|None): 
                - The request id that was provided in GetLogRequest that started this log upload. This field is mandatory, unless the message was triggered by a TriggerMessageRequest AND there is no log upload ongoing. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.LogStatusNotification
        """
        return call.LogStatusNotification(
            status=status,
            request_id=request_id,
            custom_data=custom_data
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
            status=dict_data['status'],
            request_id=dict_data.get('requestId', None),
            custom_data=dict_data.get('customData', None)
        )
