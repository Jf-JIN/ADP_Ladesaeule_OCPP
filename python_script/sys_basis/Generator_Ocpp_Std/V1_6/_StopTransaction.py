
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class stop_transaction(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.StopTransaction:
        """
        生成 StopTransaction

        参数:
            - 

        返回值:
            - call.StopTransaction
        """
        return call.StopTransaction(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.StopTransaction:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StopTransaction
        """
        return call.StopTransaction(
            
        )

