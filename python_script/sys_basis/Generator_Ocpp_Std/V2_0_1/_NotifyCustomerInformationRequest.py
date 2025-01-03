
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_customer_information_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(data, seq_no, generated_at, request_id, tbc=None, custom_data=None) -> call.NotifyCustomerInformation:
        """
        生成 NotifyCustomerInformationRequest

        参数:
            -

        返回值:
            - call.NotifyCustomerInformation
        """
        return call.NotifyCustomerInformation(
            data = data,
            seq_no = seq_no,
            generated_at = generated_at,
            request_id = request_id,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyCustomerInformation:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyCustomerInformation
        """
        return call.NotifyCustomerInformation(
            data = dict_data['data'],
            seq_no = dict_data['seqNo'],
            generated_at = dict_data['generatedAt'],
            request_id = dict_data['requestId'],
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

