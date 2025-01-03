
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_diagnostics_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(file_name=None) -> call_result.GetDiagnostics:
        """
        生成 GetDiagnosticsResponse

        参数:
            -

        返回值:
            - call_result.GetDiagnostics
        """
        return call_result.GetDiagnostics(
            file_name = file_name
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetDiagnostics:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetDiagnostics
        """
        return call_result.GetDiagnostics(
            file_name = dict_data.get('fileName', None)
        )

