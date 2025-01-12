from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenStatusNotificationResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        custom_data: dict | None = None
    ) -> call_result.StatusNotification:
        """
        生成 StatusNotificationResponse

        - 参数: 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StatusNotification:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call_result.StatusNotification
        """
        return call_result.StatusNotification(
            custom_data=dict_data.get('customData', None)
        )
