
from ocpp.v201.enums import *
from ocpp.v16 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


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

