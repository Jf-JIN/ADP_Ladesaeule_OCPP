
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class transaction_event_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.TransactionEvent:
        """
        生成 TransactionEventRequest

        参数:
        - 

        返回值:
        - call.TransactionEvent
        """
        return call.TransactionEvent(
            
        )

