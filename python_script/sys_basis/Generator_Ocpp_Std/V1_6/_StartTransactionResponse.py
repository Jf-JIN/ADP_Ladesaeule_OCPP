
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class start_transaction_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(transaction_id, id_tag_info) -> call_result.StartTransaction:
        """
        生成 StartTransactionResponse

        参数:
            -

        返回值:
            - call_result.StartTransaction
        """
        return call_result.StartTransaction(
            transaction_id = transaction_id,
            id_tag_info = id_tag_info
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StartTransaction:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.StartTransaction
        """
        return call_result.StartTransaction(
            transaction_id = dict_data['transactionId'],
            id_tag_info = dict_data['idTagInfo']
        )

