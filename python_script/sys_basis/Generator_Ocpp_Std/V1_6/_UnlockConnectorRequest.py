from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenUnlockConnectorRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int
    ) -> call.UnlockConnector:
        """
        Generate UnlockConnectorRequest

        - Args: 
            - connector_id(int): 

        - Returns:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            connector_id=connector_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.UnlockConnector:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            connector_id=dict_data['connectorId']
        )
