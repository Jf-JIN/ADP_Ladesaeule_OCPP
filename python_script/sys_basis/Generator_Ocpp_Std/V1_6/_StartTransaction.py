
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class start_transaction(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.StartTransaction:
        """
        生成 StartTransaction

        参数:
            - 

        返回值:
            - call.StartTransaction
        """
        return call.StartTransaction(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.StartTransaction:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StartTransaction
        """
        return call.StartTransaction(
            
        )

