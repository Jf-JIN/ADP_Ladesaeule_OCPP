
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class customer_information_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, report, clear, customer_certificate=None, id_token=None, customer_identifier=None, custom_data=None) -> call.CustomerInformation:
        """
        生成 CustomerInformationRequest

        参数:
            -

        返回值:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            request_id = request_id,
            report = report,
            clear = clear,
            customer_certificate = customer_certificate,
            id_token = id_token,
            customer_identifier = customer_identifier,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CustomerInformation:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            request_id = dict_data['requestId'],
            report = dict_data['report'],
            clear = dict_data['clear'],
            customer_certificate = dict_data.get('customerCertificate', None),
            id_token = dict_data.get('idToken', None),
            customer_identifier = dict_data.get('customerIdentifier', None),
            custom_data = dict_data.get('customData', None)
        )

