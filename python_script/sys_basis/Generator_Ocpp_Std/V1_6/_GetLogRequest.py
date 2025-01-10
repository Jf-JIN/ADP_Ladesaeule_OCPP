from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenGetLogRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        log: dict,
        log_type: str | Log,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call.GetLog:
        """
        Generate GetLogRequest

        - Args: 
            - log(dict): 
                - recommended to use `get_log()` to set element
            - log_type(str|Log): 
                - Enum: `DiagnosticsLog`, `SecurityLog`
                - Or use EnumClass (Recommended): `Log`. e.g. `Log.diagnostics_log`
            - request_id(int): 
            - retries(int|None): 
            - retry_interval(int|None): 

        - Returns:
            - call.GetLog
        """
        return call.GetLog(
            log=log,
            log_type=log_type,
            request_id=request_id,
            retries=retries,
            retry_interval=retry_interval
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetLog:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetLog
        """
        return call.GetLog(
            log=dict_data['log'],
            log_type=dict_data['logType'],
            request_id=dict_data['requestId'],
            retries=dict_data.get('retries', None),
            retry_interval=dict_data.get('retryInterval', None)
        )

    @staticmethod
    def get_log(
        remote_location: str,
        oldest_timestamp: str | None = None,
        latest_timestamp: str | None = None
    ) -> dict:
        """
        Get log

        - Args: 
            - remote_location(str): 
                - length limit: [1, 512]
            - oldest_timestamp(str|None): 
                - format: date-time
            - latest_timestamp(str|None): 
                - format: date-time

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'remoteLocation': remote_location
        }
        if oldest_timestamp is not None:
            temp_dict['oldestTimestamp'] = oldest_timestamp
        if latest_timestamp is not None:
            temp_dict['latestTimestamp'] = latest_timestamp
        return temp_dict
