
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class reserve_now_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.ReserveNow:
        """
        生成 ReserveNowRequest

        参数:
            - 

        返回值:
            - call.ReserveNow
        """
        return call.ReserveNow(
            
        )

