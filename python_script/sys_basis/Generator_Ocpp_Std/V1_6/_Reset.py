
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reset(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.Reset:
        """
        生成 Reset

        参数:
            - 

        返回值:
            - call.Reset
        """
        return call.Reset(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.Reset:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.Reset
        """
        return call.Reset(
            
        )

