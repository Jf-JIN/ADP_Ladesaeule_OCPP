
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class trigger_message(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(requested_message, connector_id=None) -> call.TriggerMessage:
        """
        生成 TriggerMessage

        参数:
            -

        返回值:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = requested_message,
            connector_id = connector_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.TriggerMessage:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = dict_data['requestedMessage'],
            connector_id = dict_data.get('connectorId', None)
        )

