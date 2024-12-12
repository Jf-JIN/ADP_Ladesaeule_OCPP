
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reserve_now(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.ReserveNow:
        """
        生成 ReserveNow

        参数:
        - 

        返回值:
        - call.ReserveNow
        """
        return call.ReserveNow(
            
        )

