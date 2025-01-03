
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_diagnostics_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetDiagnostics:
        """
        生成 GetDiagnosticsResponse

        参数:
            - 

        返回值:
            - call_result.GetDiagnostics
        """
        return call_result.GetDiagnostics(
            
        )

