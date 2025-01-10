from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenSignedFirmwareStatusNotificationRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | FirmwareStatus,
        request_id: int | None = None
    ) -> call.SignedFirmwareStatusNotification:
        """
        Generate SignedFirmwareStatusNotificationRequest

        - Args: 
            - status(str|FirmwareStatus): 
                - Enum: `Downloaded`, `DownloadFailed`, `Downloading`, `DownloadScheduled`, `DownloadPaused`, `Idle`, `InstallationFailed`, `Installing`, `Installed`, `InstallRebooting`, `InstallScheduled`, `InstallVerificationFailed`, `InvalidSignature`, `SignatureVerified`
                - Or use EnumClass (Recommended): `FirmwareStatus`. e.g. `FirmwareStatus.downloaded`
            - request_id(int|None): 

        - Returns:
            - call.SignedFirmwareStatusNotification
        """
        return call.SignedFirmwareStatusNotification(
            status = status,
            request_id = request_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SignedFirmwareStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SignedFirmwareStatusNotification
        """
        return call.SignedFirmwareStatusNotification(
            status = dict_data['status'],
            request_id = dict_data.get('requestId', None)
        )

