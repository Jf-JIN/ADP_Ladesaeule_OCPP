
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class clear_display_message_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call_result.ClearDisplayMessage:
        """
        生成 ClearDisplayMessageResponse

        参数:
            - 

        返回值:
            - call_result.ClearDisplayMessage
        """
        return call_result.ClearDisplayMessage(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearDisplayMessage:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.ClearDisplayMessage
        """
        return call_result.ClearDisplayMessage(
            
        )

