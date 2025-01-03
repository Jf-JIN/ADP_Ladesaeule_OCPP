
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class heartbeat_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(current_time) -> call_result.Heartbeat:
        """
        生成 HeartbeatResponse

        参数:
            -

        返回值:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time = current_time
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Heartbeat:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time = dict_data['currentTime']
        )

