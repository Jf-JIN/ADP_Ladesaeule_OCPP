
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class unlock_connector(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.UnlockConnector:
        """
        生成 UnlockConnector

        参数:
            - 

        返回值:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.UnlockConnector:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            
        )

