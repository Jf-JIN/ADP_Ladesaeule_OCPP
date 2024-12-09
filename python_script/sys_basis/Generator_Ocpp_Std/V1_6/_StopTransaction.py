
from ocpp.v201.enums import *
from ocpp.v16 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class stop_transaction(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.StopTransaction:
        """
        生成 StopTransaction

        参数:
        - 

        返回值:
        - call.StopTransaction
        """
        return call.StopTransaction(
            
        )

