from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenClearChargingProfileResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ClearChargingProfileStatus
    ) -> call_result.ClearChargingProfile:
        """
        Generate ClearChargingProfileResponse

        - Args: 
            - status(str|ClearChargingProfileStatus): 
                - Enum: `Accepted`, `Unknown`
                - Or use EnumClass (Recommended): `ClearChargingProfileStatus`. e.g. `ClearChargingProfileStatus.accepted`

        - Returns:
            - call_result.ClearChargingProfile
        """
        return call_result.ClearChargingProfile(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ClearChargingProfile
        """
        return call_result.ClearChargingProfile(
            status=dict_data['status']
        )
