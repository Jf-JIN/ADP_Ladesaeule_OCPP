
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class publish_firmware_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(location, checksum, request_id, retries=None, retry_interval=None, custom_data=None) -> call.PublishFirmware:
        """
        生成 PublishFirmwareRequest

        参数:
            -

        返回值:
            - call.PublishFirmware
        """
        return call.PublishFirmware(
            location = location,
            checksum = checksum,
            request_id = request_id,
            retries = retries,
            retry_interval = retry_interval,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.PublishFirmware:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.PublishFirmware
        """
        return call.PublishFirmware(
            location = dict_data['location'],
            checksum = dict_data['checksum'],
            request_id = dict_data['requestId'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            custom_data = dict_data.get('customData', None)
        )

