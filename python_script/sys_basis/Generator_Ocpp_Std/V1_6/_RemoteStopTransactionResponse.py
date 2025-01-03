
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class remote_stop_transaction_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.RemoteStopTransaction:
        """
        生成 RemoteStopTransactionResponse

        参数:
            - 

        返回值:
            - call_result.RemoteStopTransaction
        """
        return call_result.RemoteStopTransaction(
            
        )

