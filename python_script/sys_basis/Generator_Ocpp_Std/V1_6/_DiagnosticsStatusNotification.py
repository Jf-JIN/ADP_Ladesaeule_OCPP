
from ocpp.v201.enums import *
from ocpp.v16 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class diagnostics_status_notification(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.DiagnosticsStatusNotification:
        """
        生成 DiagnosticsStatusNotification

        参数:
        - 

        返回值:
        - call.DiagnosticsStatusNotification
        """
        return call.DiagnosticsStatusNotification(
            
        )

