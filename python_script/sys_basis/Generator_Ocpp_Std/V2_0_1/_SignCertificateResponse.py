
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class sign_certificate_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SignCertificate:
        """
        生成 SignCertificateResponse

        参数:
        - 

        返回值:
        - call_result.SignCertificate
        """
        return call_result.SignCertificate(
            
        )

