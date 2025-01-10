from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenGetDiagnosticsRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        location: str,
        retries: int | None = None,
        retry_interval: int | None = None,
        start_time: str | None = None,
        stop_time: str | None = None
    ) -> call.GetDiagnostics:
        """
        Generate GetDiagnosticsRequest

        - Args: 
            - location(str): 
                - format: uri
            - retries(int|None): 
            - retry_interval(int|None): 
            - start_time(str|None): 
                - format: date-time
            - stop_time(str|None): 
                - format: date-time

        - Returns:
            - call.GetDiagnostics
        """
        return call.GetDiagnostics(
            location = location,
            retries = retries,
            retry_interval = retry_interval,
            start_time = start_time,
            stop_time = stop_time
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetDiagnostics:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetDiagnostics
        """
        return call.GetDiagnostics(
            location = dict_data['location'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            start_time = dict_data.get('startTime', None),
            stop_time = dict_data.get('stopTime', None)
        )

