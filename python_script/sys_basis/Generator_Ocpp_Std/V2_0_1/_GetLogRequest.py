from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_log_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        log: dict,
        log_type: str | LogType,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call.GetLog:
        """
        Generate GetLogRequest

        - Args: 
            - log(dict): 
                - Log Generic class for the configuration of logging entries. 
                - recommended to use `get_log()` to set element
            - log_type(str): 
                - This contains the type of log file that the Charging Station should send. 
                - Enum: `DiagnosticsLog`, `SecurityLog`
                - Or use EnumClass (Recommended): `LogType`. e.g. `LogType.diagnostics_log`
            - request_id(int): 
                - The Id of this request 
            - retries(int|None): 
                - This specifies how many times the Charging Station must try to upload the log before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. 
            - retry_interval(int|None): 
                - The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetLog
        """
        return call.GetLog(
            log = log,
            log_type = log_type,
            request_id = request_id,
            retries = retries,
            retry_interval = retry_interval,
            custom_data = custom_data
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
            log = dict_data['log'],
            log_type = dict_data['logType'],
            request_id = dict_data['requestId'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            custom_data = dict_data.get('customData', None)
        )


    @staticmethod
    def get_log(
        remote_location: str,
        oldest_timestamp: str | None = None,
        latest_timestamp: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get log

        - Args: 
            - remote_location(str): 
                - Log. Remote_ Location. URI The URL of the location at the remote system where the log should be stored. 
                - length limit: [1, 512]
            - oldest_timestamp(str|None): 
                - Log. Oldest_ Timestamp. Date_ Time This contains the date and time of the oldest logging information to include in the diagnostics. 
                - format: date-time
            - latest_timestamp(str|None): 
                - Log. Latest_ Timestamp. Date_ Time This contains the date and time of the latest logging information to include in the diagnostics. 
                - format: date-time
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'remoteLocation': remote_location
        }
        if oldest_timestamp is not None:
            temp_dict['oldestTimestamp'] = oldest_timestamp
        if latest_timestamp is not None:
            temp_dict['latestTimestamp'] = latest_timestamp
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

