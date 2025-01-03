
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class security_event_notification_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call_result.SecurityEventNotification:
        """
        生成 SecurityEventNotificationResponse

        参数:
            - 

        返回值:
            - call_result.SecurityEventNotification
        """
        return call_result.SecurityEventNotification(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SecurityEventNotification:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.SecurityEventNotification
        """
        return call_result.SecurityEventNotification(
            
        )

