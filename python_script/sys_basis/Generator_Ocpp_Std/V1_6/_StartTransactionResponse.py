from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenStartTransactionResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id_tag_info: dict,
        transaction_id: int
    ) -> call_result.StartTransaction:
        """
        Generate StartTransactionResponse

        - Args: 
            - id_tag_info(dict): 
                - recommended to use `get_id_tag_info()` to set element
            - transaction_id(int): 

        - Returns:
            - call_result.StartTransaction
        """
        return call_result.StartTransaction(
            id_tag_info = id_tag_info,
            transaction_id = transaction_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StartTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.StartTransaction
        """
        return call_result.StartTransaction(
            id_tag_info = dict_data['idTagInfo'],
            transaction_id = dict_data['transactionId']
        )

