
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


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

