
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class stop_transaction_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.StopTransaction:
        """
        生成 StopTransactionResponse

        参数:
            - 

        返回值:
            - call_result.StopTransaction
        """
        return call_result.StopTransaction(
            
        )

