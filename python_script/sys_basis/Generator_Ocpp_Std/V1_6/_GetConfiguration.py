
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_configuration(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.GetConfiguration:
        """
        生成 GetConfiguration

        参数:
        - 

        返回值:
        - call.GetConfiguration
        """
        return call.GetConfiguration(
            
        )

