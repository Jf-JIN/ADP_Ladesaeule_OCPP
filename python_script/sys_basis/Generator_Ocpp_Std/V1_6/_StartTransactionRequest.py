from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenStartTransactionRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        id_tag: str,
        meter_start: int,
        timestamp: str,
        reservation_id: int | None = None
    ) -> call.StartTransaction:
        """
        Generate StartTransactionRequest

        - Args: 
            - connector_id(int): 
            - id_tag(str): 
                - length limit: [1, 20]
            - meter_start(int): 
            - timestamp(str): 
                - format: date-time
            - reservation_id(int|None): 

        - Returns:
            - call.StartTransaction
        """
        return call.StartTransaction(
            connector_id = connector_id,
            id_tag = id_tag,
            meter_start = meter_start,
            timestamp = timestamp,
            reservation_id = reservation_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StartTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.StartTransaction
        """
        return call.StartTransaction(
            connector_id = dict_data['connectorId'],
            id_tag = dict_data['idTag'],
            meter_start = dict_data['meterStart'],
            timestamp = dict_data['timestamp'],
            reservation_id = dict_data.get('reservationId', None)
        )

