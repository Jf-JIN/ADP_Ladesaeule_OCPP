from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_transaction_status_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        messages_in_queue: bool,
        ongoing_indicator: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetTransactionStatus:
        """
        Generate GetTransactionStatusResponse

        - Args: 
            - messages_in_queue(bool): 
                - Whether there are still message to be delivered. 
            - ongoing_indicator(bool|None): 
                - Whether the transaction is still ongoing. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetTransactionStatus
        """
        return call_result.GetTransactionStatus(
            messages_in_queue = messages_in_queue,
            ongoing_indicator = ongoing_indicator,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetTransactionStatus:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetTransactionStatus
        """
        return call_result.GetTransactionStatus(
            messages_in_queue = dict_data['messagesInQueue'],
            ongoing_indicator = dict_data.get('ongoingIndicator', None),
            custom_data = dict_data.get('customData', None)
        )

