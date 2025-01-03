
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_variables_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(set_variable_data, custom_data=None) -> call.SetVariables:
        """
        生成 SetVariablesRequest

        参数:
            -

        返回值:
            - call.SetVariables
        """
        return call.SetVariables(
            set_variable_data = set_variable_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetVariables:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetVariables
        """
        return call.SetVariables(
            set_variable_data = dict_data['setVariableData'],
            custom_data = dict_data.get('customData', None)
        )

