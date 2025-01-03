
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class delete_certificate_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status, status_info=None, custom_data=None) -> call_result.DeleteCertificate:
        """
        生成 DeleteCertificateResponse

        参数:
            -

        返回值:
            - call_result.DeleteCertificate
        """
        return call_result.DeleteCertificate(
            status = status,
            status_info = status_info,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DeleteCertificate:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.DeleteCertificate
        """
        return call_result.DeleteCertificate(
            status = dict_data['status'],
            status_info = dict_data.get('statusInfo', None),
            custom_data = dict_data.get('customData', None)
        )

