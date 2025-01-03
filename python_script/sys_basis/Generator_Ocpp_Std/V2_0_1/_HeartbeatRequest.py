
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class heartbeat_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data: dict | None = None) -> call.Heartbeat:
        """
        生成 HeartbeatRequest

        参数:
            - vendorID (str): vendor的ID, 不可为0

        返回值:
            - call.Heartbeat
        """
        return call.Heartbeat(
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Heartbeat:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.Heartbeat
        """
        return call.Heartbeat(
            custom_data=dict_data.get('customData', None)
        )
