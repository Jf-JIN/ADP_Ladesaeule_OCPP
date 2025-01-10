from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenChangeAvailabilityResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | AvailabilityStatus
    ) -> call_result.ChangeAvailability:
        """
        Generate ChangeAvailabilityResponse

        - Args: 
            - status(str|AvailabilityStatus): 
                - Enum: `Accepted`, `Rejected`, `Scheduled`
                - Or use EnumClass (Recommended): `AvailabilityStatus`. e.g. `AvailabilityStatus.accepted`

        - Returns:
            - call_result.ChangeAvailability
        """
        return call_result.ChangeAvailability(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ChangeAvailability:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ChangeAvailability
        """
        return call_result.ChangeAvailability(
            status = dict_data['status']
        )

