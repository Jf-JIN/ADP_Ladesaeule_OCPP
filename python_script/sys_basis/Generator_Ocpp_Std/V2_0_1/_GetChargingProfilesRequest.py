from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenGetChargingProfilesRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        charging_profile: dict,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.GetChargingProfiles:
        """
        Generate GetChargingProfilesRequest

        - Args: 
            - request_id(int): 
                - Reference identification that is to be used by the Charging Station in the <<reportchargingprofilesrequest, ReportChargingProfilesRequest>> when provided. 
            - charging_profile(dict): 
                - Charging_ Profile A ChargingProfile consists of ChargingSchedule, describing the amount of power or current that can be delivered per time interval. 
                - recommended to use `get_charging_profile()` to set element
            - evse_id(int|None): 
                - For which EVSE installed charging profiles SHALL be reported. If 0, only charging profiles installed on the Charging Station itself (the grid connection) SHALL be reported. If omitted, all installed charging profiles SHALL be reported. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetChargingProfiles
        """
        return call.GetChargingProfiles(
            request_id=request_id,
            charging_profile=charging_profile,
            evse_id=evse_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetChargingProfiles:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetChargingProfiles
        """
        return call.GetChargingProfiles(
            request_id=dict_data['requestId'],
            charging_profile=dict_data['chargingProfile'],
            evse_id=dict_data.get('evseId', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_charging_profile(
        charging_profile_purpose: str | ChargingProfilePurposeType | None = None,
        stack_level: int | None = None,
        charging_profile_id: list | None = None,
        charging_limit_source: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get charging profile

        - Args: 
            - charging_profile_purpose(str||None): 
                - Charging_ Profile. Charging_ Profile_ Purpose. Charging_ Profile_ Purpose_ Code Defines the purpose of the schedule transferred by this profile 
                - Enum: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`
                - Or use EnumClass (Recommended): `ChargingProfilePurposeType`. e.g. `ChargingProfilePurposeType.charging_station_external_constraints`
            - stack_level(int|None): 
                - Charging_ Profile. Stack_ Level. Counter Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. 
            - charging_profile_id(list|None): 
                - recommended to use `get_charging_profile_id()` to set element or to build a custom list.
            - charging_limit_source(list|None): 
                - length limit: [1, 4]
                - recommended to use `get_charging_limit_source()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            
        }
        if charging_profile_purpose is not None:
            temp_dict['chargingProfilePurpose'] = charging_profile_purpose
        if stack_level is not None:
            temp_dict['stackLevel'] = stack_level
        if charging_profile_id is not None:
            temp_dict['chargingProfileId'] = charging_profile_id
        if charging_limit_source is not None:
            temp_dict['chargingLimitSource'] = charging_limit_source
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
