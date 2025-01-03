
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_ev_charging_schedule_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status: GenericStatusType | str, custom_data: dict | None = None, status_info: dict | None = None, **kwargs) -> call_result.NotifyEVChargingSchedule:
        """
        生成 NotifyEVChargingScheduleResponse

        参数:
            - status(str): 状态, 可使用GenericStatusType枚举类或使用可选值: `Accepted`, `Rejected`
            - customData(dict): 自定义数据, 推荐使用 `get_custom_data()` 生成
            - statusInfo(dict): 状态信息, 推荐使用 `get_status_info()` 生成

        返回值:
            - call_result.NotifyEVChargingSchedule
        """
        return call_result.NotifyEVChargingSchedule(
            status=status or kwargs.get('status', None),
            custom_data=custom_data or kwargs.get('customData', None),
            status_info=status_info or kwargs.get('statusInfo', None)
        )

    @staticmethod
    def get_status_info(reason_code: str, custom_data: dict | None = None, additional_info: str | None = None) -> dict:
        """
        生成 statusInfo

        参数:
            - reasonCode(str): 用于说明在此响应中返回状态的原因的预定义代码,字符串不区分大小写,最大长度为20
            - customData(dict): 自定义数据, 推荐使用 `get_custom_data()` 生成
            - additionalInfo(str): 提供详细信息的附加文本, 最大长度为512

        返回值:
            - status_info(dict)
        """
        temp_dict = {
            'reasonCode': reason_code
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        return temp_dict
