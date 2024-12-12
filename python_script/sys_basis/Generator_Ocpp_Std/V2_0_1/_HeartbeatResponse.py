
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class heartbeat_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.Heartbeat:
        """
        生成 HeartbeatResponse

        参数:
        - 

        返回值:
        - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            
        )

