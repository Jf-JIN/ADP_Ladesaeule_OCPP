
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class request_stop_transaction_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.RequestStopTransaction:
        """
        生成 RequestStopTransactionResponse

        参数:
        - 

        返回值:
        - call_result.RequestStopTransaction
        """
        return call_result.RequestStopTransaction(
            
        )

