
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class status_notification_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call_result.StatusNotification:
        """
        生成 StatusNotificationResponse

        参数:
            - 

        返回值:
            - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StatusNotification:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            
        )

