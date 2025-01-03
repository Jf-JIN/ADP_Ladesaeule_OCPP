
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_local_list_version_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call_result.GetLocalListVersion:
        """
        生成 GetLocalListVersionResponse

        参数:
            - 

        返回值:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetLocalListVersion:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            
        )

