
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_configuration_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetConfiguration:
        """
        生成 GetConfigurationResponse

        参数:
        - 

        返回值:
        - call_result.GetConfiguration
        """
        return call_result.GetConfiguration(
            
        )

