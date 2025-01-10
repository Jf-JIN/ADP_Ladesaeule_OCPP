from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenSetChargingProfileResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ChargingProfileStatus
    ) -> call_result.SetChargingProfile:
        """
        Generate SetChargingProfileResponse

        - Args: 
            - status(str|ChargingProfileStatus): 
                - Enum: `Accepted`, `Rejected`, `NotSupported`
                - Or use EnumClass (Recommended): `ChargingProfileStatus`. e.g. `ChargingProfileStatus.accepted`

        - Returns:
            - call_result.SetChargingProfile
        """
        return call_result.SetChargingProfile(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SetChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SetChargingProfile
        """
        return call_result.SetChargingProfile(
            status = dict_data['status']
        )

