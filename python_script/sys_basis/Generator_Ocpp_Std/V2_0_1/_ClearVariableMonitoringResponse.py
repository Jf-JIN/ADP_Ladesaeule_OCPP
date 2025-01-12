from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenClearVariableMonitoringResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        clear_monitoring_result: list,
        custom_data: dict | None = None
    ) -> call_result.ClearVariableMonitoring:
        """
        Generate ClearVariableMonitoringResponse

        - Args: 
            - clear_monitoring_result(list): 
                - recommended to use `get_clear_monitoring_result()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.ClearVariableMonitoring
        """
        return call_result.ClearVariableMonitoring(
            clear_monitoring_result=clear_monitoring_result,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearVariableMonitoring:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ClearVariableMonitoring
        """
        return call_result.ClearVariableMonitoring(
            clear_monitoring_result=dict_data['clearMonitoringResult'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_status_info(
        reason_code: str,
        additional_info: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get status info

        - Args: 
            - reason_code(str): 
                - A predefined code for the reason why the status is returned in this response. The string is case-insensitive. 
                - length limit: [1, 20]
            - additional_info(str|None): 
                - Additional text to provide detailed information. 
                - length limit: [1, 512]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_clear_monitoring_result(
        status: str | ClearMonitoringStatusType,
        id: int,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get clear monitoring result

        - Args: 
            - status(str): 
                - Result of the clear request for this monitor, identified by its Id. 
                - Enum: `Accepted`, `Rejected`, `NotFound`
                - Or use EnumClass (Recommended): `ClearMonitoringStatusType`. e.g. `ClearMonitoringStatusType.accepted`
            - id(int): 
                - Id of the monitor of which a clear was requested. 
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'status': status,
            'id': id
        }
        if status_info is not None:
            temp_dict['statusInfo'] = status_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
