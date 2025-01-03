
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_local_list_version_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetLocalListVersion:
        """
        生成 GetLocalListVersionRequest

        参数:
            - 

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            
        )

