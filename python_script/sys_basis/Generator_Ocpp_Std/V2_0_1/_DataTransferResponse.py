
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class data_transfer_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | DataTransferStatusType,
        status_info: dict | None = None,
        data=None,
        custom_data: dict | None = None,
        **kwargs
    ) -> call_result.DataTransfer:
        """
        生成 DataTransferResponse

        参数:
        - status(str|DataTransferStatusType): 标志数据传输的成功或失败
            - `Accepted`, `Rejected`, `UnknownMessageId`, `UnknownVendorId`.
            - 或者可以使用 `DataTransferStatusType` 枚举, 例如: `DataTransferStatusType.accepted`.
        - status_info(dict): 推荐使用 `get_status_info()` 传入
        - data(any): 数据没有指定的长度或格式, 这需要由双方协商决定.
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
        - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status=status or kwargs["status"],
            data=data or kwargs.get("data", None),
            status_info=status_info or kwargs.get("statusInfo", None),
            custom_data=custom_data or kwargs.get("customData", None)
        )

    @staticmethod
    def get_status_info(reason_code: str, additional_info: str | None = None, custom_data: dict | None = None) -> dict:
        """
        生成 StatusInfo

        参数:
        - reason_code(str): 状态转到这个response的原因的预设代码, 不区分大小写, 字符长度为[1-20].
        - additional_info(str): 提供信息的额外文本, 字符长度为[1-512]
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入

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
