
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_variables_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(get_variable_data, custom_data=None) -> call.GetVariables:
        """
        生成 GetVariablesRequest

        参数:
            -

        返回值:
            - call.GetVariables
        """
        return call.GetVariables(
            get_variable_data = get_variable_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetVariables:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetVariables
        """
        return call.GetVariables(
            get_variable_data = dict_data['getVariableData'],
            custom_data = dict_data.get('customData', None)
        )

