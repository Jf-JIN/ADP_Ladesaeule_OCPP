from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenGetBaseReportResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | GenericDeviceModelStatusType,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetBaseReport:
        """
        Generate GetBaseReportResponse

        - Args: 
            - status(str): 
                - This indicates whether the Charging Station is able to accept this request. 
                - Enum: `Accepted`, `Rejected`, `NotSupported`, `EmptyResultSet`
                - Or use EnumClass (Recommended): `GenericDeviceModelStatusType`. e.g. `GenericDeviceModelStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetBaseReport
        """
        return call_result.GetBaseReport(
            status=status,
            status_info=status_info,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetBaseReport:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetBaseReport
        """
        return call_result.GetBaseReport(
            status=dict_data['status'],
            status_info=dict_data.get('statusInfo', None),
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
