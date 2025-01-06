from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class update_firmware_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        firmware: dict,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call.UpdateFirmware:
        """
        Generate UpdateFirmwareRequest

        - Args: 
            - request_id(int): 
                - The Id of this request 
            - firmware(dict): 
                - Firmware Represents a copy of the firmware that can be loaded/updated on the Charging Station. 
                - recommended to use `get_firmware()` to set element
            - retries(int|None): 
                - This specifies how many times Charging Station must try to download the firmware before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. 
            - retry_interval(int|None): 
                - The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
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
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            request_id = dict_data['requestId'],
            firmware = dict_data['firmware'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            custom_data = dict_data.get('customData', None)
        )


    @staticmethod
    def get_firmware(
        location: str,
        retrieve_date_time: str,
        install_date_time: str | None = None,
        signing_certificate: str | None = None,
        signature: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get firmware

        - Args: 
            - location(str): 
                - Firmware. Location. URI URI defining the origin of the firmware. 
                - length limit: [1, 512]
            - retrieve_date_time(str): 
                - Firmware. Retrieve. Date_ Time Date and time at which the firmware shall be retrieved. 
                - format: date-time
            - install_date_time(str|None): 
                - Firmware. Install. Date_ Time Date and time at which the firmware shall be installed. 
                - format: date-time
            - signing_certificate(str|None): 
                - Certificate with which the firmware was signed. PEM encoded X.509 certificate. 
                - length limit: [1, 5500]
            - signature(str|None): 
                - Firmware. Signature. Signature Base64 encoded firmware signature. 
                - length limit: [1, 800]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'location': location,
            'retrieveDateTime': retrieve_date_time
        }
        if install_date_time is not None:
            temp_dict['installDateTime'] = install_date_time
        if signing_certificate is not None:
            temp_dict['signingCertificate'] = signing_certificate
        if signature is not None:
            temp_dict['signature'] = signature
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

