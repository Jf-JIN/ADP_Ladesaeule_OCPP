
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class data_transfer_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(vendor_id: str, message_id: str | None = None, data=None,
                 custom_data: dict | None = None, **kwargs) -> call.DataTransfer:
        """
        生成 DataTransferRequest

        参数:
        - vendor_id(str): 用于标识供应商的特别操作, 字符长度为[1-255]
        - message_id(str): 可用来表明特定的信息或操作, 字符长度为[1-50]
        - data(any): 数据没有指定的长度或格式, 这需要由双方协商决定.
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
        - call.DataTransfer
        """
        return call.DataTransfer(
            vendor_id=vendor_id or kwargs["vendorId"],
            message_id=message_id or kwargs.get("messageId", None),
            data=data or kwargs.get("data", None),
            custom_data=custom_data or kwargs.get("customData", None)
        )
