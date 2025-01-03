
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class start_transaction_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.StartTransaction:
        """
        生成 StartTransactionResponse

        参数:
            - 

        返回值:
            - call_result.StartTransaction
        """
        return call_result.StartTransaction(
            
        )

