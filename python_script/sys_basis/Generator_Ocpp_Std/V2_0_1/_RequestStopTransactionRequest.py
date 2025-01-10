from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenRequestStopTransactionRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        transaction_id: str,
        custom_data: dict | None = None
    ) -> call.RequestStopTransaction:
        """
        Generate RequestStopTransactionRequest

        - Args: 
            - transaction_id(str): 
                - The identifier of the transaction which the Charging Station is requested to stop. 
                - length limit: [1, 36]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.RequestStopTransaction
        """
        return call.RequestStopTransaction(
            transaction_id=transaction_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RequestStopTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.RequestStopTransaction
        """
        return call.RequestStopTransaction(
            transaction_id=dict_data['transactionId'],
            custom_data=dict_data.get('customData', None)
        )
