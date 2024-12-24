
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class boot_notification_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(interval: int, status: str | RegistrationStatusType, current_time: str,
                 status_info: dict,  custom_data: dict | None = None, **kwargs) -> call_result.BootNotification:
        """
        生成 BootNotificationResponse

        参数:
        - current_time(str): 包含CSMS现在的时间，格式是"date-time"
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入
        - interval(int):当 Status 的值为 Accepted时，interval 表示心跳的时间间隔，单位是秒。
            -当 Status 的值不是 Accepted（如 Rejected 或其他状态）时，interval 不再表示心跳间隔，而是指定了在发送下一个 BootNotification 请求之前的最小等待时间。
        - status(str|RegistrationStatusType): 类型 候选:
            - `Accepted`, `Pending`, `Rejected`.
            - 或者可以使用 `RegistrationStatusType` 枚举, 例如: `RegistrationStatusType.accepted` .
        - status_info(dict): 推荐使用 `get_status_info()`传入

        返回值:
        - call_result.BootNotification
        """
        return call_result.BootNotification(
            current_time=current_time or kwargs.get("current_time", None),
            custom_data=custom_data or kwargs.get("custom_data", None),
            interval=interval or kwargs.get("interval", None),
            status_info=status_info or kwargs.get("status_info", None),
            status=status or kwargs.get("status", None)
        )

    @staticmethod
    def get_status_info(reason_code: str, additional_info: str, custom_data: dict | None = None) -> dict:

        """
        生成 StatusInfo

        参数:
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入
        - reason_code(str): 在此响应中返回状态的原因的预定义代码, 字符串不区分大小写, 长度为 [1-20] 个字符
        - additional_info(str): 提供详细信息的附加文本, 长度为 [1-512] 个字符 
       
        返回值:
        - status_info(dict)
        """

        temp_dict = {
            "reasonCode": reason_code
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if additional_info is not None:
            temp_dict["additionalInfo"] = additional_info
        return temp_dict
