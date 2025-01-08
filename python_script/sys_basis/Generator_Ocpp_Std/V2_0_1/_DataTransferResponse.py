from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class data_transfer_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | DataTransferStatusType,
        status_info: dict | None = None,
        data: None = None,
        custom_data: dict | None = None
    ) -> call_result.DataTransfer:
        """
        生成 DataTransferResponse

        - 参数: 
            - status(str): 
                - 标志数据传输的成功或失败 
                - 枚举值: `Accepted`, `Rejected`, `UnknownMessageId`, `UnknownVendorId`
                - 或使用枚举类(推荐)`DataTransferStatusType`. e.g. `DataTransferStatusType.accepted`
            - status_info(dict|None): 
                - 提供有关状态的更多信息的元素. 
                - 推荐使用 `get_status_info()` 传入
            - data: 
                - 没有指定长度或格式的数据, 以响应请求. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status=status,
            status_info=status_info,
            data=data,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DataTransfer:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status=dict_data['status'],
            status_info=dict_data.get('statusInfo', None),
            data=dict_data.get('data', None),
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
                - 用于说明在此响应中返回状态的原因的预定义代码. 该字符串不区分大小写. 
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
