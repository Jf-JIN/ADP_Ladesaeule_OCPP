
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_certificate_status_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call_result.GetCertificateStatus:
        """
        生成 GetCertificateStatusResponse

        参数:
            - 

        返回值:
            - call_result.GetCertificateStatus
        """
        return call_result.GetCertificateStatus(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetCertificateStatus:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetCertificateStatus
        """
        return call_result.GetCertificateStatus(
            
        )

