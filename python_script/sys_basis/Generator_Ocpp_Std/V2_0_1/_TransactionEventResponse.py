
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class transaction_event_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.TransactionEvent:
        """
        生成 TransactionEventResponse

        参数:
            - 

        返回值:
            - call_result.TransactionEvent
        """
        return call_result.TransactionEvent(
            
        )

