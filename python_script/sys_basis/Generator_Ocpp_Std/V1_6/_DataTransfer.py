
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class data_transfer(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.DataTransfer:
        """
        生成 DataTransfer

        参数:
        - 

        返回值:
        - call.DataTransfer
        """
        return call.DataTransfer(
            
        )

