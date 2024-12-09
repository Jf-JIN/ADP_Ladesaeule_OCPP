
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class log_status_notification_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.LogStatusNotification:
        """
        生成 LogStatusNotificationRequest

        参数:
        - 

        返回值:
        - call.LogStatusNotification
        """
        return call.LogStatusNotification(
            
        )

