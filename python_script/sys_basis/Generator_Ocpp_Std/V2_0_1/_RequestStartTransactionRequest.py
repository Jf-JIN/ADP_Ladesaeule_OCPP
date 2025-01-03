
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class request_start_transaction_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.RequestStartTransaction:
        """
        生成 RequestStartTransactionRequest

        参数:
            - 

        返回值:
            - call.RequestStartTransaction
        """
        return call.RequestStartTransaction(
            
        )

