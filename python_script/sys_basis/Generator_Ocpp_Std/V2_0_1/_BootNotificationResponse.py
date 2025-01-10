from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenBootNotificationResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        current_time: str,
        interval: int,
        status: str | RegistrationStatusType,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.BootNotification:
        """
        生成 BootNotificationResponse

        - 参数: 
            - current_time(str): 
                - 包含CSMS现在的时间. 
                - 格式: date-time
            - interval(int): 
                - 当 <<cmn_registrationstatusenumtype,Status>> 被接受时, 其中包含心跳间隔(以秒为单位). 如果 CSMS 返回 Accepted 以外的内容, 则间隔字段的值指示发送下一个 BootNotification 请求之前的最短等待时间. 
            - status(str): 
                - 这包含充电站是否已在 CSMS 中注册. 
                - 枚举值: `Accepted`, `Pending`, `Rejected`
                - 或使用枚举类(推荐)`RegistrationStatusType`. e.g. `RegistrationStatusType.accepted`
            - status_info(dict|None): 
                - 提供有关状态的更多信息的元素. 
                - 推荐使用 `get_status_info()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            current_time=current_time,
            interval=interval,
            status=status,
            status_info=status_info,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.BootNotification:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call_result.BootNotification
        """
        return call_result.BootNotification(
            current_time=dict_data['currentTime'],
            interval=dict_data['interval'],
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
                - 用于说明在此响应中返回状态的原因的预定义代码. 字符串不区分大小写. 
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
