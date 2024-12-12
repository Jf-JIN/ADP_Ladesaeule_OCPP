
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class diagnostics_status_notification_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.DiagnosticsStatusNotification:
        """
        生成 DiagnosticsStatusNotificationResponse

        参数:
        - 

        返回值:
        - call_result.DiagnosticsStatusNotification
        """
        return call_result.DiagnosticsStatusNotification(
            
        )

