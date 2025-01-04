
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class heartbeat_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(current_time: str, custom_data: dict | None = None) -> call_result.Heartbeat:
        """
        生成 HeartbeatResponse

        参数:
            - current_time(str): 现在的时间, 格式为date-time
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time=current_time,
            custom_data=custom_data
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
            current_time=dict_data['currentTime'],
            custom_data=dict_data.get('customData', None)
        )
