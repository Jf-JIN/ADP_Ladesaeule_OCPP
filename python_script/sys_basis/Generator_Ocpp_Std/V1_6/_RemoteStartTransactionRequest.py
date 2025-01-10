from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenRemoteStartTransactionRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id_tag: str,
        connector_id: int | None = None,
        charging_profile: dict | None = None
    ) -> call.RemoteStartTransaction:
        """
        Generate RemoteStartTransactionRequest

        - Args: 
            - id_tag(str): 
                - length limit: [1, 20]
            - connector_id(int|None): 
            - charging_profile(dict|None): 
                - recommended to use `get_charging_profile()` to set element

        - Returns:
            - call.RemoteStartTransaction
        """
        return call.RemoteStartTransaction(
            id_tag=id_tag,
            connector_id=connector_id,
            charging_profile=charging_profile
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RemoteStartTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.RemoteStartTransaction
        """
        return call.RemoteStartTransaction(
            id_tag=dict_data['idTag'],
            connector_id=dict_data.get('connectorId', None),
            charging_profile=dict_data.get('chargingProfile', None)
        )
