
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class data_transfer_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(status, status_info=None, data=None, custom_data=None) -> call_result.DataTransfer:
        """
        生成 DataTransferResponse

        参数:
            -

        返回值:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status = status,
            status_info = status_info,
            data = data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DataTransfer:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status = dict_data['status'],
            status_info = dict_data.get('statusInfo', None),
            data = dict_data.get('data', None),
            custom_data = dict_data.get('customData', None)
        )

