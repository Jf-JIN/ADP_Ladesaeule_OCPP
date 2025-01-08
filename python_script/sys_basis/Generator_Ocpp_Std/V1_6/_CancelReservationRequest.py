from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class cancel_reservation_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        reservation_id: int
    ) -> call.CancelReservation:
        """
        Generate CancelReservationRequest

        - Args: 
            - reservation_id(int): 

        - Returns:
            - call.CancelReservation
        """
        return call.CancelReservation(
            reservation_id = reservation_id
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
            reservation_id = dict_data['reservationId']
        )

