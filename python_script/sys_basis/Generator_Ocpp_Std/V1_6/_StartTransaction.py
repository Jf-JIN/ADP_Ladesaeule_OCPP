
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class start_transaction(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, id_tag, meter_start, timestamp, reservation_id=None) -> call.StartTransaction:
        """
        生成 StartTransaction

        参数:
            -

        返回值:
            - call.StartTransaction
        """
        return call.StartTransaction(
            connector_id = connector_id,
            id_tag = id_tag,
            meter_start = meter_start,
            timestamp = timestamp,
            reservation_id = reservation_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StartTransaction:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StartTransaction
        """
        return call.StartTransaction(
            connector_id = dict_data['connectorId'],
            id_tag = dict_data['idTag'],
            meter_start = dict_data['meterStart'],
            timestamp = dict_data['timestamp'],
            reservation_id = dict_data.get('reservationId', None)
        )

