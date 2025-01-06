from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_transaction_status_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        transaction_id: str | None = None,
        custom_data: dict | None = None
    ) -> call.GetTransactionStatus:
        """
        Generate GetTransactionStatusRequest

        - Args: 
            - transaction_id(str|None): 
                - The Id of the transaction for which the status is requested. 
                - length limit: [1, 36]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetTransactionStatus
        """
        return call.GetTransactionStatus(
            transaction_id = transaction_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetTransactionStatus:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetTransactionStatus
        """
        return call.GetTransactionStatus(
            transaction_id = dict_data.get('transactionId', None),
            custom_data = dict_data.get('customData', None)
        )

