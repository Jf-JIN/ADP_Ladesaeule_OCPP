
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class remote_start_transaction_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call_result.RemoteStartTransaction:
        """
        生成 RemoteStartTransactionResponse

        参数:
            - 

        返回值:
            - call_result.RemoteStartTransaction
        """
        return call_result.RemoteStartTransaction(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.RemoteStartTransaction:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.RemoteStartTransaction
        """
        return call_result.RemoteStartTransaction(
            
        )

