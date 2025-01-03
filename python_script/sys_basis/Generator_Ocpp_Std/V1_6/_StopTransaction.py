
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class stop_transaction(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(meter_stop, timestamp, transaction_id, reason=None, id_tag=None, transaction_data=None) -> call.StopTransaction:
        """
        生成 StopTransaction

        参数:
            -

        返回值:
            - call.StopTransaction
        """
        return call.StopTransaction(
            meter_stop = meter_stop,
            timestamp = timestamp,
            transaction_id = transaction_id,
            reason = reason,
            id_tag = id_tag,
            transaction_data = transaction_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StopTransaction:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StopTransaction
        """
        return call.StopTransaction(
            meter_stop = dict_data['meterStop'],
            timestamp = dict_data['timestamp'],
            transaction_id = dict_data['transactionId'],
            reason = dict_data.get('reason', None),
            id_tag = dict_data.get('idTag', None),
            transaction_data = dict_data.get('transactionData', None)
        )

