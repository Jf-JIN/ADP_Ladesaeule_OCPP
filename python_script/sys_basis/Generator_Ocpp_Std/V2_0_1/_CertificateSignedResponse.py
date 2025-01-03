
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class certificate_signed_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.CertificateSigned:
        """
        生成 CertificateSignedResponse

        参数:
            - 

        返回值:
            - call_result.CertificateSigned
        """
        return call_result.CertificateSigned(
            
        )

