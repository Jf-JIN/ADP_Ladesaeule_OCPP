
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class change_configuration_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(status) -> call_result.ChangeConfiguration:
        """
        生成 ChangeConfigurationResponse

        参数:
            -

        返回值:
            - call_result.ChangeConfiguration
        """
        return call_result.ChangeConfiguration(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ChangeConfiguration:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.ChangeConfiguration
        """
        return call_result.ChangeConfiguration(
            status = dict_data['status']
        )

