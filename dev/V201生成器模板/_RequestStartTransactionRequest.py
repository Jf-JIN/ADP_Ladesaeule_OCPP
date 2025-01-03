
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class request_start_transaction_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id_token, remote_start_id, evse_id=None, group_id_token=None, charging_profile=None, custom_data=None) -> call.RequestStartTransaction:
        """
        生成 RequestStartTransactionRequest

        参数:
            -

        返回值:
            - call.RequestStartTransaction
        """
        return call.RequestStartTransaction(
            id_token = id_token,
            remote_start_id = remote_start_id,
            evse_id = evse_id,
            group_id_token = group_id_token,
            charging_profile = charging_profile,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RequestStartTransaction:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.RequestStartTransaction
        """
        return call.RequestStartTransaction(
            id_token = dict_data['idToken'],
            remote_start_id = dict_data['remoteStartId'],
            evse_id = dict_data.get('evseId', None),
            group_id_token = dict_data.get('groupIdToken', None),
            charging_profile = dict_data.get('chargingProfile', None),
            custom_data = dict_data.get('customData', None)
        )

