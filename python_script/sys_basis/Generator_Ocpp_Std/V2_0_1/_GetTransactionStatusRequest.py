
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_transaction_status_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetTransactionStatus:
        """
        生成 GetTransactionStatusRequest

        参数:
            - 

        返回值:
            - call.GetTransactionStatus
        """
        return call.GetTransactionStatus(
            
        )

