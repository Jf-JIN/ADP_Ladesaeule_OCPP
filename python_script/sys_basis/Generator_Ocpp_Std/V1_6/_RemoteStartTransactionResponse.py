
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class remote_start_transaction_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.RemoteStartTransaction:
        """
        生成 RemoteStartTransactionResponse

        参数:
            - 

        返回值:
            - call_result.RemoteStartTransaction
        """
        return call_result.RemoteStartTransaction(
            
        )

