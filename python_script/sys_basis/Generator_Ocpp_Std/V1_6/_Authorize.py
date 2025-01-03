
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class authorize(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.Authorize:
        """
        生成 Authorize

        参数:
            - 

        返回值:
            - call.Authorize
        """
        return call.Authorize(
            
        )

