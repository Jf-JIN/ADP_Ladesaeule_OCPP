from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class cancel_reservation_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        reservation_id: int,
        custom_data: dict | None = None
    ) -> call.CancelReservation:
        """
        Generate CancelReservationRequest

        - Args: 
            - reservation_id(int): 
                - Id of the reservation to cancel. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.CancelReservation
        """
        return call.CancelReservation(
            reservation_id = reservation_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CancelReservation:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.CancelReservation
        """
        return call.CancelReservation(
            reservation_id = dict_data['reservationId'],
            custom_data = dict_data.get('customData', None)
        )

