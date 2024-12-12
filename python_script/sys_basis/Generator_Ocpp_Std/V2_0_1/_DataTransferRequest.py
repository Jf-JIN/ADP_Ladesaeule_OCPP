
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class data_transfer_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.DataTransfer:
        """
        生成 DataTransferRequest

        参数:
        - 

        返回值:
        - call.DataTransfer
        """
        return call.DataTransfer(
            
        )

