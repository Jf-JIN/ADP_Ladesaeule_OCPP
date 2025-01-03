
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class change_configuration(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.ChangeConfiguration:
        """
        生成 ChangeConfiguration

        参数:
            - 

        返回值:
            - call.ChangeConfiguration
        """
        return call.ChangeConfiguration(
            
        )

