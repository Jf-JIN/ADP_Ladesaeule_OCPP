
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class meter_values_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate() -> call_result.MeterValues:
        """
        生成 MeterValuesResponse

        参数:
            -

        返回值:
            - call_result.MeterValues
        """
        return call_result.MeterValues(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.MeterValues:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.MeterValues
        """
        return call_result.MeterValues(
            
        )

