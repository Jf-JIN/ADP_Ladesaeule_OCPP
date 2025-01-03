
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_display_messages_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, message_info=None, tbc=None, custom_data=None) -> call.NotifyDisplayMessages:
        """
        生成 NotifyDisplayMessagesRequest

        参数:
            -

        返回值:
            - call.NotifyDisplayMessages
        """
        return call.NotifyDisplayMessages(
            request_id = request_id,
            message_info = message_info,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyDisplayMessages:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyDisplayMessages
        """
        return call.NotifyDisplayMessages(
            request_id = dict_data['requestId'],
            message_info = dict_data.get('messageInfo', None),
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

