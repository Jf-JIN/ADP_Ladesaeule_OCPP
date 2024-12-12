
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class install_certificate_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.InstallCertificate:
        """
        生成 InstallCertificateRequest

        参数:
        - 

        返回值:
        - call.InstallCertificate
        """
        return call.InstallCertificate(
            
        )

