
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class meter_values(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.MeterValues:
        """
        生成 MeterValues

        参数:
            - 

        返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            
        )

