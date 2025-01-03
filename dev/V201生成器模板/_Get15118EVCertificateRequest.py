
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get15118_ev_certificate_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(iso15118_schema_version, action, exi_request, custom_data=None) -> call.Get15118EVCertificate:
        """
        生成 Get15118EVCertificateRequest

        参数:
            -

        返回值:
            - call.Get15118EVCertificate
        """
        return call.Get15118EVCertificate(
            iso15118_schema_version = iso15118_schema_version,
            action = action,
            exi_request = exi_request,
            custom_data = custom_data
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
            iso15118_schema_version = dict_data['iso15118SchemaVersion'],
            action = dict_data['action'],
            exi_request = dict_data['exiRequest'],
            custom_data = dict_data.get('customData', None)
        )

