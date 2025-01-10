from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenCancelReservationResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | CancelReservationStatus
    ) -> call_result.CancelReservation:
        """
        Generate CancelReservationResponse

        - Args: 
            - status(str|CancelReservationStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `CancelReservationStatus`. e.g. `CancelReservationStatus.accepted`

        - Returns:
            - call_result.CancelReservation
        """
        return call_result.CancelReservation(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.CancelReservation:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.CancelReservation
        """
        return call_result.CancelReservation(
            status=dict_data['status']
        )
