
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class delete_certificate_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(certificate_hash_data, custom_data=None) -> call.DeleteCertificate:
        """
        生成 DeleteCertificateRequest

        参数:
            -

        返回值:
            - call.DeleteCertificate
        """
        return call.DeleteCertificate(
            certificate_hash_data = certificate_hash_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.DeleteCertificate:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.DeleteCertificate
        """
        return call.DeleteCertificate(
            certificate_hash_data = dict_data['certificateHashData'],
            custom_data = dict_data.get('customData', None)
        )

