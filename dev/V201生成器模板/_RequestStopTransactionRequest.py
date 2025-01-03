
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class request_stop_transaction_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(transaction_id, custom_data=None) -> call.RequestStopTransaction:
        """
        生成 RequestStopTransactionRequest

        参数:
            -

        返回值:
            - call.RequestStopTransaction
        """
        return call.RequestStopTransaction(
            transaction_id = transaction_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RequestStopTransaction:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.RequestStopTransaction
        """
        return call.RequestStopTransaction(
            transaction_id = dict_data['transactionId'],
            custom_data = dict_data.get('customData', None)
        )

