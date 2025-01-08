from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_charging_profiles_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | GetChargingProfileStatusType,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetChargingProfiles:
        """
        Generate GetChargingProfilesResponse

        - Args: 
            - status(str): 
                - This indicates whether the Charging Station is able to process this request and will send <<reportchargingprofilesrequest, ReportChargingProfilesRequest>> messages. 
                - Enum: `Accepted`, `NoProfiles`
                - Or use EnumClass (Recommended): `GetChargingProfileStatusType`. e.g. `GetChargingProfileStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetChargingProfiles
        """
        return call_result.GetChargingProfiles(
            status = status,
            status_info = status_info,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetChargingProfiles:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetChargingProfiles
        """
        return call_result.GetChargingProfiles(
            status = dict_data['status'],
            status_info = dict_data.get('statusInfo', None),
            custom_data = dict_data.get('customData', None)
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
        temp_dict:dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

