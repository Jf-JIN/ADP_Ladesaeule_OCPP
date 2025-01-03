
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class heartbeat(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.Heartbeat:
        """
        生成 Heartbeat

        参数:
            - 

        返回值:
            - call.Heartbeat
        """
        return call.Heartbeat(
            
        )

