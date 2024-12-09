
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


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

