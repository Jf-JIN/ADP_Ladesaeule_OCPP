
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class trigger_message_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(requested_message, evse=None, custom_data=None) -> call.TriggerMessage:
        """
        生成 TriggerMessageRequest

        参数:
            -

        返回值:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = requested_message,
            evse = evse,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.TriggerMessage:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = dict_data['requestedMessage'],
            evse = dict_data.get('evse', None),
            custom_data = dict_data.get('customData', None)
        )

