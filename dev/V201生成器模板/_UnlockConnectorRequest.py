
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class unlock_connector_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(evse_id, connector_id, custom_data=None) -> call.UnlockConnector:
        """
        生成 UnlockConnectorRequest

        参数:
            -

        返回值:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            evse_id = evse_id,
            connector_id = connector_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.UnlockConnector:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.UnlockConnector
        """
        return call.UnlockConnector(
            evse_id = dict_data['evseId'],
            connector_id = dict_data['connectorId'],
            custom_data = dict_data.get('customData', None)
        )

