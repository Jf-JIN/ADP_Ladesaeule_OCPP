from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenReserveNowResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ReservationStatus
    ) -> call_result.ReserveNow:
        """
        Generate ReserveNowResponse

        - Args: 
            - status(str|ReservationStatus): 
                - Enum: `Accepted`, `Faulted`, `Occupied`, `Rejected`, `Unavailable`
                - Or use EnumClass (Recommended): `ReservationStatus`. e.g. `ReservationStatus.accepted`

        - Returns:
            - call_result.ReserveNow
        """
        return call_result.ReserveNow(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ReserveNow:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ReserveNow
        """
        return call_result.ReserveNow(
            status=dict_data['status']
        )
