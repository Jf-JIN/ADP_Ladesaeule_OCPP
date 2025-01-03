
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reset(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.Reset:
        """
        生成 Reset

        参数:
            - 

        返回值:
            - call.Reset
        """
        return call.Reset(
            
        )

