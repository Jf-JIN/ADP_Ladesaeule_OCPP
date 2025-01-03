
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_variables_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(set_variable_result, custom_data=None) -> call_result.SetVariables:
        """
        生成 SetVariablesResponse

        参数:
            -

        返回值:
            - call_result.SetVariables
        """
        return call_result.SetVariables(
            set_variable_result = set_variable_result,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SetVariables:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.SetVariables
        """
        return call_result.SetVariables(
            set_variable_result = dict_data['setVariableResult'],
            custom_data = dict_data.get('customData', None)
        )

