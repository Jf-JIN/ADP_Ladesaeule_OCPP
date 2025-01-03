
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_transaction_status_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(transaction_id=None, custom_data=None) -> call.GetTransactionStatus:
        """
        生成 GetTransactionStatusRequest

        参数:
            -

        返回值:
            - call.GetTransactionStatus
        """
        return call.GetTransactionStatus(
            transaction_id = transaction_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetTransactionStatus:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetTransactionStatus
        """
        return call.GetTransactionStatus(
            transaction_id = dict_data.get('transactionId', None),
            custom_data = dict_data.get('customData', None)
        )

