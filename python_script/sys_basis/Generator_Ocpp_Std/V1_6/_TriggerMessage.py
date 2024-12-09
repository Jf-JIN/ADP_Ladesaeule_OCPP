
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class trigger_message(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.TriggerMessage:
        """
        生成 TriggerMessage

        参数:
        - 

        返回值:
        - call.TriggerMessage
        """
        return call.TriggerMessage(
            
        )

