
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class meter_values(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, meter_value, transaction_id=None) -> call.MeterValues:
        """
        生成 MeterValues

        参数:
            -

        返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            connector_id = connector_id,
            meter_value = meter_value,
            transaction_id = transaction_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.MeterValues:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            connector_id = dict_data['connectorId'],
            meter_value = dict_data['meterValue'],
            transaction_id = dict_data.get('transactionId', None)
        )

