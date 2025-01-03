
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class sign_certificate_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(csr, certificate_type=None, custom_data=None) -> call.SignCertificate:
        """
        生成 SignCertificateRequest

        参数:
            -

        返回值:
            - call.SignCertificate
        """
        return call.SignCertificate(
            csr = csr,
            certificate_type = certificate_type,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SignCertificate:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SignCertificate
        """
        return call.SignCertificate(
            csr = dict_data['csr'],
            certificate_type = dict_data.get('certificateType', None),
            custom_data = dict_data.get('customData', None)
        )

