
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_installed_certificate_ids_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status, status_info=None, certificate_hash_data_chain=None, custom_data=None) -> call_result.GetInstalledCertificateIds:
        """
        生成 GetInstalledCertificateIdsResponse

        参数:
            -

        返回值:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            status = status,
            status_info = status_info,
            certificate_hash_data_chain = certificate_hash_data_chain,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetInstalledCertificateIds:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            status = dict_data['status'],
            status_info = dict_data.get('statusInfo', None),
            certificate_hash_data_chain = dict_data.get('certificateHashDataChain', None),
            custom_data = dict_data.get('customData', None)
        )

