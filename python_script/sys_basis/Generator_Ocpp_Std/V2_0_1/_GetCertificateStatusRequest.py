
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_certificate_status_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetCertificateStatus:
        """
        生成 GetCertificateStatusRequest

        参数:
        - 

        返回值:
        - call.GetCertificateStatus
        """
        return call.GetCertificateStatus(
            
        )

