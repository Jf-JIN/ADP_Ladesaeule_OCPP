from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenSignedUpdateFirmwareResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | UpdateFirmwareStatus
    ) -> call_result.SignedUpdateFirmware:
        """
        Generate SignedUpdateFirmwareResponse

        - Args: 
            - status(str|UpdateFirmwareStatus): 
                - Enum: `Accepted`, `Rejected`, `AcceptedCanceled`, `InvalidCertificate`, `RevokedCertificate`
                - Or use EnumClass (Recommended): `UpdateFirmwareStatus`. e.g. `UpdateFirmwareStatus.accepted`

        - Returns:
            - call_result.SignedUpdateFirmware
        """
        return call_result.SignedUpdateFirmware(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SignedUpdateFirmware:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SignedUpdateFirmware
        """
        return call_result.SignedUpdateFirmware(
            status=dict_data['status']
        )
