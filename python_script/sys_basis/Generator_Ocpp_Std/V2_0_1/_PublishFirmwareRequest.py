from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenPublishFirmwareRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        location: str,
        checksum: str,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call.PublishFirmware:
        """
        Generate PublishFirmwareRequest

        - Args: 
            - location(str): 
                - This contains a string containing a URI pointing to a location from which to retrieve the firmware. 
                - length limit: [1, 512]
            - checksum(str): 
                - The MD5 checksum over the entire firmware file as a hexadecimal string of length 32.  
                - length limit: [1, 32]
            - request_id(int): 
                - The Id of the request. 
            - retries(int|None): 
                - This specifies how many times Charging Station must try to download the firmware before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. 
            - retry_interval(int|None): 
                - The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.PublishFirmware
        """
        return call.PublishFirmware(
            location=location,
            checksum=checksum,
            request_id=request_id,
            retries=retries,
            retry_interval=retry_interval,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.PublishFirmware:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.PublishFirmware
        """
        return call.PublishFirmware(
            location=dict_data['location'],
            checksum=dict_data['checksum'],
            request_id=dict_data['requestId'],
            retries=dict_data.get('retries', None),
            retry_interval=dict_data.get('retryInterval', None),
            custom_data=dict_data.get('customData', None)
        )
