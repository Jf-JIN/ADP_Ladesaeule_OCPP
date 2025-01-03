
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_certificate_status_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(ocsp_request_data, custom_data=None) -> call.GetCertificateStatus:
        """
        生成 GetCertificateStatusRequest

        参数:
            -

        返回值:
            - call.GetCertificateStatus
        """
        return call.GetCertificateStatus(
            ocsp_request_data = ocsp_request_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetCertificateStatus:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetCertificateStatus
        """
        return call.GetCertificateStatus(
            ocsp_request_data = dict_data['ocspRequestData'],
            custom_data = dict_data.get('customData', None)
        )

