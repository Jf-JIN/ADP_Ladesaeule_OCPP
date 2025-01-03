
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reserve_now(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, expiry_date, id_tag, reservation_id, parent_id_tag=None) -> call.ReserveNow:
        """
        生成 ReserveNow

        参数:
            -

        返回值:
            - call.ReserveNow
        """
        return call.ReserveNow(
            connector_id = connector_id,
            expiry_date = expiry_date,
            id_tag = id_tag,
            reservation_id = reservation_id,
            parent_id_tag = parent_id_tag
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReserveNow:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ReserveNow
        """
        return call.ReserveNow(
            connector_id = dict_data['connectorId'],
            expiry_date = dict_data['expiryDate'],
            id_tag = dict_data['idTag'],
            reservation_id = dict_data['reservationId'],
            parent_id_tag = dict_data.get('parentIdTag', None)
        )

