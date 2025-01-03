
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_transaction_status_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(messages_in_queue, ongoing_indicator=None, custom_data=None) -> call_result.GetTransactionStatus:
        """
        生成 GetTransactionStatusResponse

        参数:
            -

        返回值:
            - call_result.GetTransactionStatus
        """
        return call_result.GetTransactionStatus(
            messages_in_queue = messages_in_queue,
            ongoing_indicator = ongoing_indicator,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetTransactionStatus:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetTransactionStatus
        """
        return call_result.GetTransactionStatus(
            messages_in_queue = dict_data['messagesInQueue'],
            ongoing_indicator = dict_data.get('ongoingIndicator', None),
            custom_data = dict_data.get('customData', None)
        )

