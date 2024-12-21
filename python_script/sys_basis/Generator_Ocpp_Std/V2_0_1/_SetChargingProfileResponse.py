
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_charging_profile_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status: str | ChargingProfileStatus, status_info: dict | None = None, custom_data: dict | None = None, **kwargs) -> call_result.SetChargingProfile:
        """
        生成 SetChargingProfileResponse

        参数:
        - status(str): 返回充电站是否能够成功处理消息. 这并不能保证时间表会被严格遵守. 充电站可能还需要考虑其他限制. 
            - `Accepted` `Rejected`
            - 可以使用 `ChargingProfileStatus` 枚举, 例如: `ChargingProfileStatus.accepted`
        - status_info(dict): 提供有关状态的更多信息的元素. 推荐使用 `get_status_info` 方法
        - custom_data: 自定义数据, 推荐使用 `get_custom_data` 方法

        返回值:
        - call_result.SetChargingProfile
        """
        return call_result.SetChargingProfile(
            status=status,
            status_info=status_info or kwargs.get('statusInfo', None),
            custom_data=custom_data or kwargs.get('customData', None)
        )

    @staticmethod
    def get_status_info(reason_code: str, additional_info: str | None = None, custom_data: dict | None = None) -> dict:
        """
        获取 status_info

        参数: 
        - reason_code: 原因代码, 用于说明在此响应中返回状态的原因的预定义代码. 该字符串不区分大小写. 长度: [1,20]
        - additional_info: 附加信息, 提供详细信息的附加文本. 长度: [0,512]
        - custom_data: 自定义数据, 推荐使用 `get_custom_data` 方法

        返回值:
        - dict
        """
        temp = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp['additionalInfo'] = additional_info
        if custom_data is not None:
            temp['customData'] = custom_data
        return temp
