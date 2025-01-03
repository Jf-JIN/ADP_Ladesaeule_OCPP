
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get15118_ev_certificate_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call.Get15118EVCertificate:
        """
        生成 Get15118EVCertificateRequest

        参数:
            - 

        返回值:
            - call.Get15118EVCertificate
        """
        return call.Get15118EVCertificate(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.Get15118EVCertificate:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.Get15118EVCertificate
        """
        return call.Get15118EVCertificate(
            
        )

