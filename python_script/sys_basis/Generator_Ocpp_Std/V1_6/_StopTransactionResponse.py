
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class stop_transaction_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(id_tag_info=None) -> call_result.StopTransaction:
        """
        生成 StopTransactionResponse

        参数:
            -

        返回值:
            - call_result.StopTransaction
        """
        return call_result.StopTransaction(
            id_tag_info = id_tag_info
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StopTransaction:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.StopTransaction
        """
        return call_result.StopTransaction(
            id_tag_info = dict_data.get('idTagInfo', None)
        )

