from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenUpdateFirmwareResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        
    ) -> call_result.UpdateFirmware:
        """
        Generate UpdateFirmwareResponse

        - Args: 
            

        - Returns:
            - call_result.UpdateFirmware
        """
        return call_result.UpdateFirmware(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.UpdateFirmware:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.UpdateFirmware
        """
        return call_result.UpdateFirmware(
            
        )
