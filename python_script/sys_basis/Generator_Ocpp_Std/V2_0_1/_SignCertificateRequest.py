
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class sign_certificate_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SignCertificate:
        """
        生成 SignCertificateRequest

        参数:
        - 

        返回值:
        - call.SignCertificate
        """
        return call.SignCertificate(
            
        )

