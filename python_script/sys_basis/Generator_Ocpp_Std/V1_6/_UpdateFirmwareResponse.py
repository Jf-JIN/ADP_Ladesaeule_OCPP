
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class update_firmware_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.UpdateFirmware:
        """
        生成 UpdateFirmwareResponse

        参数:
            - 

        返回值:
            - call_result.UpdateFirmware
        """
        return call_result.UpdateFirmware(
            
        )

