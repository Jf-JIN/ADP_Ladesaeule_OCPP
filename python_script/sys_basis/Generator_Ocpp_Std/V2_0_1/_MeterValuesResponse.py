

from ocpp.v201 import call_result
from ._Base import *


class meter_values_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data: dict | None = None) -> call_result.MeterValues:
        """
        生成 MeterValuesResponse

        参数:
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - call_result.MeterValues
        """
        return call_result.MeterValues(
            custom_data=custom_data
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
            custom_data=dict_data.get('customData', None)
        )
