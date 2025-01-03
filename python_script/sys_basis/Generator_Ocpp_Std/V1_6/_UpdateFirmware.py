
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class update_firmware(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(location, retrieve_date, retries=None, retry_interval=None) -> call.UpdateFirmware:
        """
        生成 UpdateFirmware

        参数:
            -

        返回值:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            location = location,
            retrieve_date = retrieve_date,
            retries = retries,
            retry_interval = retry_interval
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.UpdateFirmware:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            location = dict_data['location'],
            retrieve_date = dict_data['retrieveDate'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None)
        )

