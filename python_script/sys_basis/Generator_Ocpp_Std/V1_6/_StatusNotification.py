
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class status_notification(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.StatusNotification:
        """
        生成 StatusNotification

        参数:
            - 

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            
        )

