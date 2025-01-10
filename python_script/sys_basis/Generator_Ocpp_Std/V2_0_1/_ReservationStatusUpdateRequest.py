from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenReservationStatusUpdateRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        reservation_id: int,
        reservation_update_status: str | ReservationUpdateStatusType,
        custom_data: dict | None = None
    ) -> call.ReservationStatusUpdate:
        """
        Generate ReservationStatusUpdateRequest

        - Args: 
            - reservation_id(int): 
                - The ID of the reservation. 
            - reservation_update_status(str): 
                - The updated reservation status. 
                - Enum: `Expired`, `Removed`
                - Or use EnumClass (Recommended): `ReservationUpdateStatusType`. e.g. `ReservationUpdateStatusType.expired`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ReservationStatusUpdate
        """
        return call.ReservationStatusUpdate(
            reservation_id=reservation_id,
            reservation_update_status=reservation_update_status,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReservationStatusUpdate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ReservationStatusUpdate
        """
        return call.ReservationStatusUpdate(
            reservation_id=dict_data['reservationId'],
            reservation_update_status=dict_data['reservationUpdateStatus'],
            custom_data=dict_data.get('customData', None)
        )
