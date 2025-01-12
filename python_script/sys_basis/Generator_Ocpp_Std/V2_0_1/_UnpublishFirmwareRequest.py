from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenUnpublishFirmwareRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        checksum: str,
        custom_data: dict | None = None
    ) -> call.UnpublishFirmware:
        """
        Generate UnpublishFirmwareRequest

        - Args: 
            - checksum(str): 
                - The MD5 checksum over the entire firmware file as a hexadecimal string of length 32.  
                - length limit: [1, 32]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.UnpublishFirmware
        """
        return call.UnpublishFirmware(
            checksum=checksum,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.UnpublishFirmware:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.UnpublishFirmware
        """
        return call.UnpublishFirmware(
            checksum=dict_data['checksum'],
            custom_data=dict_data.get('customData', None)
        )
