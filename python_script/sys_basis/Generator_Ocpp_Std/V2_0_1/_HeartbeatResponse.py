
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class heartbeat_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(current_time: str | None = None, custom_data: dict | None = None, **kwargs) -> call_result.Heartbeat:
        """
        生成 HeartbeatResponse

        参数:
            - current_time(str): 现在的时间, 格式为date-time
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time=current_time or kwargs["currentTime"],
            custom_data=custom_data or kwargs.get("customData", None)
        )
