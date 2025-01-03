
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_installed_certificate_ids_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetInstalledCertificateIds:
        """
        生成 GetInstalledCertificateIdsResponse

        参数:
            - 

        返回值:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            
        )

