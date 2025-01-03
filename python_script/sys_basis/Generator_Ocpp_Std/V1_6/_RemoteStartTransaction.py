
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class remote_start_transaction(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.RemoteStartTransaction:
        """
        生成 RemoteStartTransaction

        参数:
            - 

        返回值:
            - call.RemoteStartTransaction
        """
        return call.RemoteStartTransaction(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.RemoteStartTransaction:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.RemoteStartTransaction
        """
        return call.RemoteStartTransaction(
            
        )

