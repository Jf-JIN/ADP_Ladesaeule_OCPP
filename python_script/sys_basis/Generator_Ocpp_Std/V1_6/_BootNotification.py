
from ocpp.v201.enums import *
from ocpp.v16 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class boot_notification(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.BootNotification:
        """
        生成 BootNotification

        参数:
        - 

        返回值:
        - call.BootNotification
        """
        return call.BootNotification(
            
        )

