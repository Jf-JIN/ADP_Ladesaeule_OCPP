
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class certificate_signed_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(certificate_chain, certificate_type=None, custom_data=None) -> call.CertificateSigned:
        """
        生成 CertificateSignedRequest

        参数:
            -

        返回值:
            - call.CertificateSigned
        """
        return call.CertificateSigned(
            certificate_chain = certificate_chain,
            certificate_type = certificate_type,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CertificateSigned:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.CertificateSigned
        """
        return call.CertificateSigned(
            certificate_chain = dict_data['certificateChain'],
            certificate_type = dict_data.get('certificateType', None),
            custom_data = dict_data.get('customData', None)
        )

