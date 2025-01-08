from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_ev_charging_needs_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | NotifyEVChargingNeedsStatusType,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyEVChargingNeeds:
        """
        生成 NotifyEVChargingNeedsResponse

        - 参数: 
            - status(str): 
                - 返回 CSMS 是否能够成功处理消息. 这并不意味着当前的充电配置文件可以满足 evChargingNeeds. 
                - 枚举值: `Accepted`, `Rejected`, `Processing`
                - 或使用枚举类(推荐)`NotifyEVChargingNeedsStatusType`. e.g. `NotifyEVChargingNeedsStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - 推荐使用 `get_status_info()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call_result.NotifyEVChargingNeeds
        """
        return call_result.NotifyEVChargingNeeds(
            status=status,
            status_info=status_info,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.NotifyEVChargingNeeds:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call_result.NotifyEVChargingNeeds
        """
        return call_result.NotifyEVChargingNeeds(
            status=dict_data['status'],
            status_info=dict_data.get('statusInfo', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_status_info(
        reason_code: str,
        additional_info: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 status info

        - 参数: 
            - reason_code(str): 
                - 用于说明在此响应中返回状态的原因的预定义代码,字符串不区分大小写
                - 长度范围: [1, 20]
            - additional_info(str|None): 
                - 提供详细信息的附加文本. 
                - 长度范围: [1, 512]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
