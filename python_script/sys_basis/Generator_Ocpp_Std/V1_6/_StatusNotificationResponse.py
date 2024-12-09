
from ocpp.v201.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class status_notification_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.StatusNotification:
        """
        生成 StatusNotificationResponse

        参数:
        - 

        返回值:
        - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            
        )

