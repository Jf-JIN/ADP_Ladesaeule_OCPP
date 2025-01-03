
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class reserve_now_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.ReserveNow:
        """
        生成 ReserveNowResponse

        参数:
            - 

        返回值:
            - call_result.ReserveNow
        """
        return call_result.ReserveNow(
            
        )

