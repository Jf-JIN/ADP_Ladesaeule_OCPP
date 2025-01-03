
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_display_message_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(message, custom_data=None) -> call.SetDisplayMessage:
        """
        生成 SetDisplayMessageRequest

        参数:
            -

        返回值:
            - call.SetDisplayMessage
        """
        return call.SetDisplayMessage(
            message = message,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetDisplayMessage:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetDisplayMessage
        """
        return call.SetDisplayMessage(
            message = dict_data['message'],
            custom_data = dict_data.get('customData', None)
        )

