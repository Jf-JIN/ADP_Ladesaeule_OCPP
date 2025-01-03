
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class update_firmware_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, firmware, retries=None, retry_interval=None, custom_data=None) -> call.UpdateFirmware:
        """
        生成 UpdateFirmwareRequest

        参数:
            -

        返回值:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            request_id = request_id,
            firmware = firmware,
            retries = retries,
            retry_interval = retry_interval,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.UpdateFirmware:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            request_id = dict_data['requestId'],
            firmware = dict_data['firmware'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            custom_data = dict_data.get('customData', None)
        )

