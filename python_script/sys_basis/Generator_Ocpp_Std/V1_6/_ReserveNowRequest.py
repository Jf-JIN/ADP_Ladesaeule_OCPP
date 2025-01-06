from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reserve_now_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        expiry_date: str,
        id_tag: str,
        reservation_id: int,
        parent_id_tag: str | None = None
    ) -> call.ReserveNow:
        """
        Generate ReserveNowRequest

        - Args: 
            - connector_id(int): 
            - expiry_date(str): 
                - format: date-time
            - id_tag(str): 
                - length limit: [1, 20]
            - reservation_id(int): 
            - parent_id_tag(str|None): 
                - length limit: [1, 20]

        - Returns:
            - call.ReserveNow
        """
        return call.ReserveNow(
            connector_id = connector_id,
            expiry_date = expiry_date,
            id_tag = id_tag,
            reservation_id = reservation_id,
            parent_id_tag = parent_id_tag
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReserveNow:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ReserveNow
        """
        return call.ReserveNow(
            connector_id = dict_data['connectorId'],
            expiry_date = dict_data['expiryDate'],
            id_tag = dict_data['idTag'],
            reservation_id = dict_data['reservationId'],
            parent_id_tag = dict_data.get('parentIdTag', None)
        )

