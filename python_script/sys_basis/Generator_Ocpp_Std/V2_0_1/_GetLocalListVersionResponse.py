
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_local_list_version_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetLocalListVersion:
        """
        生成 GetLocalListVersionResponse

        参数:
        - 

        返回值:
        - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            
        )

