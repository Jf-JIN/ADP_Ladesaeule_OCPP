from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenFirmwareStatusNotificationRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | FirmwareStatus
    ) -> call.FirmwareStatusNotification:
        """
        Generate FirmwareStatusNotificationRequest

        - Args: 
            - status(str|FirmwareStatus): 
                - Enum: `Downloaded`, `DownloadFailed`, `Downloading`, `Idle`, `InstallationFailed`, `Installing`, `Installed`
                - Or use EnumClass (Recommended): `FirmwareStatus`. e.g. `FirmwareStatus.downloaded`

        - Returns:
            - call.FirmwareStatusNotification
        """
        return call.FirmwareStatusNotification(
            status=status
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
            status=dict_data['status']
        )
