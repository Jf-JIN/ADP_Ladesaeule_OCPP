
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class remote_stop_transaction(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.RemoteStopTransaction:
        """
        生成 RemoteStopTransaction

        参数:
            - 

        返回值:
            - call.RemoteStopTransaction
        """
        return call.RemoteStopTransaction(
            
        )

