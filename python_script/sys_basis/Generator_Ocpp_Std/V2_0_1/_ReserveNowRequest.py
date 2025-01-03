
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class reserve_now_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id, expiry_date_time, id_token, connector_type=None, evse_id=None, group_id_token=None, custom_data=None) -> call.ReserveNow:
        """
        生成 ReserveNowRequest

        参数:
            -

        返回值:
            - call.ReserveNow
        """
        return call.ReserveNow(
            id = id,
            expiry_date_time = expiry_date_time,
            id_token = id_token,
            connector_type = connector_type,
            evse_id = evse_id,
            group_id_token = group_id_token,
            custom_data = custom_data
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
            id = dict_data['id'],
            expiry_date_time = dict_data['expiryDateTime'],
            id_token = dict_data['idToken'],
            connector_type = dict_data.get('connectorType', None),
            evse_id = dict_data.get('evseId', None),
            group_id_token = dict_data.get('groupIdToken', None),
            custom_data = dict_data.get('customData', None)
        )

