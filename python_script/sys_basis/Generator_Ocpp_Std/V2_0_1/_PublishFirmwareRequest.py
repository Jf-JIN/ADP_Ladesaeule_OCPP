
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class publish_firmware_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.PublishFirmware:
        """
        生成 PublishFirmwareRequest

        参数:
            - 

        返回值:
            - call.PublishFirmware
        """
        return call.PublishFirmware(
            
        )

