
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_diagnostics(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.GetDiagnostics:
        """
        生成 GetDiagnostics

        参数:
        - 

        返回值:
        - call.GetDiagnostics
        """
        return call.GetDiagnostics(
            
        )

