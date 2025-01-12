from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenSignedUpdateFirmwareRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        request_id: int,
        firmware: dict,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call.SignedUpdateFirmware:
        """
        Generate SignedUpdateFirmwareRequest

        - Args: 
            - request_id(int): 
            - firmware(dict): 
                - recommended to use `get_firmware()` to set element
            - retries(int|None): 
            - retry_interval(int|None): 

        - Returns:
            - call.SignedUpdateFirmware
        """
        return call.SignedUpdateFirmware(
            request_id=request_id,
            firmware=firmware,
            retries=retries,
            retry_interval=retry_interval
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SignedUpdateFirmware:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SignedUpdateFirmware
        """
        return call.SignedUpdateFirmware(
            request_id=dict_data['requestId'],
            firmware=dict_data['firmware'],
            retries=dict_data.get('retries', None),
            retry_interval=dict_data.get('retryInterval', None)
        )

    @staticmethod
    def get_firmware(
        location: str,
        retrieve_date_time: str,
        signing_certificate: str,
        signature: str,
        install_date_time: str | None = None
    ) -> dict:
        """
        Get firmware

        - Args: 
            - location(str): 
                - length limit: [1, 512]
            - retrieve_date_time(str): 
                - format: date-time
            - signing_certificate(str): 
                - length limit: [1, 5500]
            - signature(str): 
                - length limit: [1, 800]
            - install_date_time(str|None): 
                - format: date-time

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'location': location,
            'retrieveDateTime': retrieve_date_time,
            'signingCertificate': signing_certificate,
            'signature': signature
        }
        if install_date_time is not None:
            temp_dict['installDateTime'] = install_date_time
        return temp_dict
