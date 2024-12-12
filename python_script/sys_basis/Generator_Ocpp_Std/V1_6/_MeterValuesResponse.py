
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class meter_values_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.MeterValues:
        """
        生成 MeterValuesResponse

        参数:
        - 

        返回值:
        - call_result.MeterValues
        """
        return call_result.MeterValues(
            
        )

