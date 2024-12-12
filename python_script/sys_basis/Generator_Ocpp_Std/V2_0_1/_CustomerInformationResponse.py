
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class customer_information_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.CustomerInformation:
        """
        生成 CustomerInformationResponse

        参数:
        - 

        返回值:
        - call_result.CustomerInformation
        """
        return call_result.CustomerInformation(
            
        )

