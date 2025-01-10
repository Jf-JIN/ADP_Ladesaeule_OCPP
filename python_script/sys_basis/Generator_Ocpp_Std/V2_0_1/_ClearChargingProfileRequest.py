from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenClearChargingProfileRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        charging_profile_id: int | None = None,
        charging_profile_criteria: dict | None = None,
        custom_data: dict | None = None
    ) -> call.ClearChargingProfile:
        """
        Generate ClearChargingProfileRequest

        - Args: 
            - charging_profile_id(int|None): 
                - The Id of the charging profile to clear. 
            - charging_profile_criteria(dict|None): 
                - Charging_ Profile A ChargingProfile consists of a ChargingSchedule, describing the amount of power or current that can be delivered per time interval. 
                - recommended to use `get_charging_profile_criteria()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            charging_profile_id=charging_profile_id,
            charging_profile_criteria=charging_profile_criteria,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            charging_profile_id=dict_data.get('chargingProfileId', None),
            charging_profile_criteria=dict_data.get('chargingProfileCriteria', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_charging_profile_criteria(
        evse_id: int | None = None,
        charging_profile_purpose: str | ChargingProfilePurposeType | None = None,
        stack_level: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get charging profile criteria

        - Args: 
            - evse_id(int|None): 
                - Identified_ Object. MRID. Numeric_ Identifier Specifies the id of the EVSE for which to clear charging profiles. An evseId of zero (0) specifies the charging profile for the overall Charging Station. Absence of this parameter means the clearing applies to all charging profiles that match the other criteria in the request. 
            - charging_profile_purpose(str||None): 
                - Charging_ Profile. Charging_ Profile_ Purpose. Charging_ Profile_ Purpose_ Code Specifies to purpose of the charging profiles that will be cleared, if they meet the other criteria in the request. 
                - Enum: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`
                - Or use EnumClass (Recommended): `ChargingProfilePurposeType`. e.g. `ChargingProfilePurposeType.charging_station_external_constraints`
            - stack_level(int|None): 
                - Charging_ Profile. Stack_ Level. Counter Specifies the stackLevel for which charging profiles will be cleared, if they meet the other criteria in the request. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            
        }
        if evse_id is not None:
            temp_dict['evseId'] = evse_id
        if charging_profile_purpose is not None:
            temp_dict['chargingProfilePurpose'] = charging_profile_purpose
        if stack_level is not None:
            temp_dict['stackLevel'] = stack_level
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
