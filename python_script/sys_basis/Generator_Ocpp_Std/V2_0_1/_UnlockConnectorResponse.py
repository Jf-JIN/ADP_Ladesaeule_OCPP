
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class unlock_connector_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.UnlockConnector:
        """
        生成 UnlockConnectorResponse

        参数:
            - 

        返回值:
            - call_result.UnlockConnector
        """
        return call_result.UnlockConnector(
            
        )

