from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenUpdateFirmwareRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        location: str,
        retrieve_date: str,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call.UpdateFirmware:
        """
        Generate UpdateFirmwareRequest

        - Args: 
            - location(str): 
                - format: uri
            - retrieve_date(str): 
                - format: date-time
            - retries(int|None): 
            - retry_interval(int|None): 

        - Returns:
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
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.UpdateFirmware
        """
        return call.UpdateFirmware(
            location = dict_data['location'],
            retrieve_date = dict_data['retrieveDate'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None)
        )

