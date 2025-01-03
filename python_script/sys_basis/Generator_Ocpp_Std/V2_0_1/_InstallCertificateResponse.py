
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class install_certificate_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.InstallCertificate:
        """
        生成 InstallCertificateResponse

        参数:
            - 

        返回值:
            - call_result.InstallCertificate
        """
        return call_result.InstallCertificate(
            
        )

