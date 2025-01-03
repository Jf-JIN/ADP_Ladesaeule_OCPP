
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class data_transfer_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.DataTransfer:
        """
        生成 DataTransferResponse

        参数:
            - 

        返回值:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            
        )

