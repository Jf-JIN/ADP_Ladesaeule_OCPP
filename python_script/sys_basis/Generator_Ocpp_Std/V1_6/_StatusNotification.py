
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class status_notification(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.StatusNotification:
        """
        生成 StatusNotification

        参数:
            - 

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.StatusNotification:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            
        )

