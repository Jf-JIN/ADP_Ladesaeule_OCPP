
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_local_list_version(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.GetLocalListVersion:
        """
        生成 GetLocalListVersion

        参数:
            - 

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            
        )

