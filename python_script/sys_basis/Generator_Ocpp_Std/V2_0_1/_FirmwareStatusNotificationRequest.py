from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenFirmwareStatusNotificationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | FirmwareStatusType,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.FirmwareStatusNotification:
        """
        Generate FirmwareStatusNotificationRequest

        - Args: 
            - status(str): 
                - This contains the progress status of the firmware installation. 
                - Enum: `Downloaded`, `DownloadFailed`, `Downloading`, `DownloadScheduled`, `DownloadPaused`, `Idle`, `InstallationFailed`, `Installing`, `Installed`, `InstallRebooting`, `InstallScheduled`, `InstallVerificationFailed`, `InvalidSignature`, `SignatureVerified`
                - Or use EnumClass (Recommended): `FirmwareStatusType`. e.g. `FirmwareStatusType.downloaded`
            - request_id(int|None): 
                - The request id that was provided in the UpdateFirmwareRequest that started this firmware update. This field is mandatory, unless the message was triggered by a TriggerMessageRequest AND there is no firmware update ongoing. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            status=status,
            request_id=request_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.FirmwareStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            status=dict_data['status'],
            request_id=dict_data.get('requestId', None),
            custom_data=dict_data.get('customData', None)
        )
