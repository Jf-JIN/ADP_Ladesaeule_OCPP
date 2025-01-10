from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenRemoteStopTransactionRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        transaction_id: int
    ) -> call.RemoteStopTransaction:
        """
        Generate RemoteStopTransactionRequest

        - Args: 
            - transaction_id(int): 

        - Returns:
            - call.RemoteStopTransaction
        """
        return call.RemoteStopTransaction(
            transaction_id = transaction_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RemoteStopTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.RemoteStopTransaction
        """
        return call.RemoteStopTransaction(
            transaction_id = dict_data['transactionId']
        )

