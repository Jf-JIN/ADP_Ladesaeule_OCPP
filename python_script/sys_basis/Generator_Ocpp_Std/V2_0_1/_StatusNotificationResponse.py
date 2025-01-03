

from ocpp.v201 import call_result
from ._Base import *


class status_notification_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data: dict | None = None, **kwargs) -> call_result.StatusNotification:
        """
        生成 StatusNotificationResponse

        参数:
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            custom_data=custom_data or kwargs.get("custom_data", None),

        )
