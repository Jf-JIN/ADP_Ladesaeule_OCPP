
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get15118_ev_certificate_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.Get15118EVCertificate:
        """
        生成 Get15118EVCertificateResponse

        参数:
        - 

        返回值:
        - call_result.Get15118EVCertificate
        """
        return call_result.Get15118EVCertificate(
            
        )

