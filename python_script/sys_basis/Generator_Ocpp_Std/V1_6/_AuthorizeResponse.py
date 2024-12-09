
from ocpp.v201.enums import *
from ocpp.v16 import call_result
from ._Base import *
from const.Ocpp_Struct_Standard.V1_6.OCPP_Valid_Const import *


class authorize_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.Authorize:
        """
        生成 AuthorizeResponse

        参数:
        - 

        返回值:
        - call_result.Authorize
        """
        return call_result.Authorize(
            
        )

