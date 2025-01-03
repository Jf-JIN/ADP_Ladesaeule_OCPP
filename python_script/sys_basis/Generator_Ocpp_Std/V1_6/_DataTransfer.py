
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class data_transfer(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(vendor_id, message_id=None, data=None) -> call.DataTransfer:
        """
        生成 DataTransfer

        参数:
            -

        返回值:
            - call.DataTransfer
        """
        return call.DataTransfer(
            vendor_id = vendor_id,
            message_id = message_id,
            data = data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.DataTransfer:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.DataTransfer
        """
        return call.DataTransfer(
            vendor_id = dict_data['vendorId'],
            message_id = dict_data.get('messageId', None),
            data = dict_data.get('data', None)
        )

