
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class authorize_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id_token, certificate=None, iso15118_certificate_hash_data=None, custom_data=None) -> call.Authorize:
        """
        生成 AuthorizeRequest

        参数:
            -

        返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_token = id_token,
            certificate = certificate,
            iso15118_certificate_hash_data = iso15118_certificate_hash_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Authorize:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_token = dict_data['idToken'],
            certificate = dict_data.get('certificate', None),
            iso15118_certificate_hash_data = dict_data.get('iso15118CertificateHashData', None),
            custom_data = dict_data.get('customData', None)
        )

