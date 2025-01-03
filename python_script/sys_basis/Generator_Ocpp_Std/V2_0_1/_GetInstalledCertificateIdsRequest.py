
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_installed_certificate_ids_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(certificate_type=None, custom_data=None) -> call.GetInstalledCertificateIds:
        """
        生成 GetInstalledCertificateIdsRequest

        参数:
            -

        返回值:
            - call.GetInstalledCertificateIds
        """
        return call.GetInstalledCertificateIds(
            certificate_type = certificate_type,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetInstalledCertificateIds:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetInstalledCertificateIds
        """
        return call.GetInstalledCertificateIds(
            certificate_type = dict_data.get('certificateType', None),
            custom_data = dict_data.get('customData', None)
        )

