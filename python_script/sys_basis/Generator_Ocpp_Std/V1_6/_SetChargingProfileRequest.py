from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenSetChargingProfileRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        cs_charging_profiles: dict
    ) -> call.SetChargingProfile:
        """
        Generate SetChargingProfileRequest

        - Args: 
            - connector_id(int): 
            - cs_charging_profiles(dict): 
                - recommended to use `get_cs_charging_profiles()` to set element

        - Returns:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id=connector_id,
            cs_charging_profiles=cs_charging_profiles
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id=dict_data['connectorId'],
            cs_charging_profiles=dict_data['csChargingProfiles']
        )

    @staticmethod
    def get_charging_schedule_period(
        start_period: int,
        limit: int | float,
        number_phases: int | None = None
    ) -> dict:
        """
        Get charging schedule period

        - Args: 
            - start_period(int): 
            - limit(int|float): 
            - number_phases(int|None): 

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'startPeriod': start_period,
            'limit': limit
        }
        if number_phases is not None:
            temp_dict['numberPhases'] = number_phases
        return temp_dict

    @staticmethod
    def get_charging_schedule(
        charging_rate_unit: str | ChargingRateUnitType,
        charging_schedule_period: list,
        duration: int | None = None,
        start_schedule: str | None = None,
        min_charging_rate: int | float | None = None
    ) -> dict:
        """
        Get charging schedule

        - Args: 
            - charging_rate_unit(str|ChargingRateUnitType): 
                - Enum: `A`, `W`
                - Or use EnumClass (Recommended): `ChargingRateUnitType`. e.g. `ChargingRateUnitType.a`
            - charging_schedule_period(list): 
                - recommended to use `get_charging_schedule_period()` to set element or to build a custom list.
            - duration(int|None): 
            - start_schedule(str|None): 
                - format: date-time
            - min_charging_rate(int|float|None): 

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'chargingRateUnit': charging_rate_unit,
            'chargingSchedulePeriod': charging_schedule_period
        }
        if duration is not None:
            temp_dict['duration'] = duration
        if start_schedule is not None:
            temp_dict['startSchedule'] = start_schedule
        if min_charging_rate is not None:
            temp_dict['minChargingRate'] = min_charging_rate
        return temp_dict

    @staticmethod
    def get_cs_charging_profiles(
        charging_profile_id: int,
        stack_level: int,
        charging_profile_purpose: str | ChargingProfilePurposeType,
        charging_profile_kind: str | ChargingProfileKindType,
        charging_schedule: dict,
        transaction_id: int | None = None,
        recurrency_kind: str | RecurrencyKind | None = None,
        valid_from: str | None = None,
        valid_to: str | None = None
    ) -> dict:
        """
        Get cs charging profiles

        - Args: 
            - charging_profile_id(int): 
            - stack_level(int): 
            - charging_profile_purpose(str|ChargingProfilePurposeType): 
                - Enum: `ChargePointMaxProfile`, `TxDefaultProfile`, `TxProfile`
                - Or use EnumClass (Recommended): `ChargingProfilePurposeType`. e.g. `ChargingProfilePurposeType.charge_point_max_profile`
            - charging_profile_kind(str|ChargingProfileKindType): 
                - Enum: `Absolute`, `Recurring`, `Relative`
                - Or use EnumClass (Recommended): `ChargingProfileKindType`. e.g. `ChargingProfileKindType.absolute`
            - charging_schedule(dict): 
                - recommended to use `get_charging_schedule()` to set element
            - transaction_id(int|None): 
            - recurrency_kind(str|RecurrencyKind|None): 
                - Enum: `Daily`, `Weekly`
                - Or use EnumClass (Recommended): `RecurrencyKind`. e.g. `RecurrencyKind.daily`
            - valid_from(str|None): 
                - format: date-time
            - valid_to(str|None): 
                - format: date-time

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'chargingProfileId': charging_profile_id,
            'stackLevel': stack_level,
            'chargingProfilePurpose': charging_profile_purpose,
            'chargingProfileKind': charging_profile_kind,
            'chargingSchedule': charging_schedule
        }
        if transaction_id is not None:
            temp_dict['transactionId'] = transaction_id
        if recurrency_kind is not None:
            temp_dict['recurrencyKind'] = recurrency_kind
        if valid_from is not None:
            temp_dict['validFrom'] = valid_from
        if valid_to is not None:
            temp_dict['validTo'] = valid_to
        return temp_dict
