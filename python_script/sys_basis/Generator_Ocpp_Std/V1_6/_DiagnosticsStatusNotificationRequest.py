from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenDiagnosticsStatusNotificationRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | DiagnosticsStatus
    ) -> call.DiagnosticsStatusNotification:
        """
        Generate DiagnosticsStatusNotificationRequest

        - Args: 
            - status(str|DiagnosticsStatus): 
                - Enum: `Idle`, `Uploaded`, `UploadFailed`, `Uploading`
                - Or use EnumClass (Recommended): `DiagnosticsStatus`. e.g. `DiagnosticsStatus.idle`

        - Returns:
            - call.DiagnosticsStatusNotification
        """
        return call.DiagnosticsStatusNotification(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.DiagnosticsStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.DiagnosticsStatusNotification
        """
        return call.DiagnosticsStatusNotification(
            status=dict_data['status']
        )
