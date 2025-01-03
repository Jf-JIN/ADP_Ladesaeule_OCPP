
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class reset_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(status) -> call_result.Reset:
        """
        生成 ResetResponse

        参数:
            -

        返回值:
            - call_result.Reset
        """
        return call_result.Reset(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Reset:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.Reset
        """
        return call_result.Reset(
            status = dict_data['status']
        )

