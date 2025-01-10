from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenUnlockConnectorRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        evse_id: int,
        connector_id: int,
        custom_data: dict | None = None
    ) -> call.UnlockConnector:
        """
        Generate UnlockConnectorRequest

        - Args: 
            - evse_id(int): 
                - This contains the identifier of the EVSE for which a connector needs to be unlocked. 
            - connector_id(int): 
                - This contains the identifier of the connector that needs to be unlocked. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            evse_id=evse_id,
            connector_id=connector_id,
            custom_data=custom_data
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
            evse_id=dict_data['evseId'],
            connector_id=dict_data['connectorId'],
            custom_data=dict_data.get('customData', None)
        )
