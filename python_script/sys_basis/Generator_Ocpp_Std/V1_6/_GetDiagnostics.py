
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_diagnostics(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.GetDiagnostics:
        """
        生成 GetDiagnostics

        参数:
            - 

        返回值:
            - call.GetDiagnostics
        """
        return call.GetDiagnostics(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.GetDiagnostics:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetDiagnostics
        """
        return call.GetDiagnostics(
            
        )

