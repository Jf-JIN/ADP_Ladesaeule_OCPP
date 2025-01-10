from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenRequestStartTransactionRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        id_token: dict,
        remote_start_id: int,
        evse_id: int | None = None,
        group_id_token: dict | None = None,
        charging_profile: dict | None = None,
        custom_data: dict | None = None
    ) -> call.RequestStartTransaction:
        """
        Generate RequestStartTransactionRequest

        - Args: 
            - id_token(dict): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_id_token()` to set element
            - remote_start_id(int): 
                - Id given by the server to this start request. The Charging Station might return this in the <<transactioneventrequest, TransactionEventRequest>>, letting the server know which transaction was started for this request. Use to start a transaction. 
            - evse_id(int|None): 
                - Number of the EVSE on which to start the transaction. EvseId SHALL be > 0 
            - group_id_token(dict|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_group_id_token()` to set element
            - charging_profile(dict|None): 
                - Charging_ Profile A ChargingProfile consists of ChargingSchedule, describing the amount of power or current that can be delivered per time interval. 
                - recommended to use `get_charging_profile()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.RequestStartTransaction
        """
        return call.RequestStartTransaction(
            id_token=id_token,
            remote_start_id=remote_start_id,
            evse_id=evse_id,
            group_id_token=group_id_token,
            charging_profile=charging_profile,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.RequestStartTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.RequestStartTransaction
        """
        return call.RequestStartTransaction(
            id_token=dict_data['idToken'],
            remote_start_id=dict_data['remoteStartId'],
            evse_id=dict_data.get('evseId', None),
            group_id_token=dict_data.get('groupIdToken', None),
            charging_profile=dict_data.get('chargingProfile', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get additional info

        - Args: 
            - additional_id_token(str): 
                - This field specifies the additional IdToken. 
                - length limit: [1, 36]
            - type(str): 
                - This defines the type of the additionalIdToken. This is a custom type, so the implementation needs to be agreed upon by all involved parties. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_group_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get group id token

        - Args: 
            - id_token(str): 
                - IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. 
                - length limit: [1, 36]
            - type(str): 
                - Enumeration of possible idToken types. 
                - Enum: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - Or use EnumClass (Recommended): `IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_additional_info()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get additional info

        - Args: 
            - additional_id_token(str): 
                - This field specifies the additional IdToken. 
                - length limit: [1, 36]
            - type(str): 
                - This defines the type of the additionalIdToken. This is a custom type, so the implementation needs to be agreed upon by all involved parties. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get id token

        - Args: 
            - id_token(str): 
                - IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. 
                - length limit: [1, 36]
            - type(str): 
                - Enumeration of possible idToken types. 
                - Enum: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - Or use EnumClass (Recommended): `IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_additional_info()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_schedule_period(
        start_period: int,
        limit: int | float,
        number_phases: int | None = None,
        phase_to_use: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get charging schedule period

        - Args: 
            - start_period(int): 
                - Charging_ Schedule_ Period. Start_ Period. Elapsed_ Time Start of the period, in seconds from the start of schedule. The value of StartPeriod also defines the stop time of the previous period. 
            - limit(int|float): 
                - Charging_ Schedule_ Period. Limit. Measure Charging rate limit during the schedule period, in the applicable chargingRateUnit, for example in Amperes (A) or Watts (W). Accepts at most one digit fraction (e.g. 8.1). 
            - number_phases(int|None): 
                - Charging_ Schedule_ Period. Number_ Phases. Counter The number of phases that can be used for charging. If a number of phases is needed, numberPhases=3 will be assumed unless another number is given. 
            - phase_to_use(int|None): 
                - Values: 1..3, Used if numberPhases=1 and if the EVSE is capable of switching the phase connected to the EV, i.e. ACPhaseSwitchingSupported is defined and true. It's not allowed unless both conditions above are true. If both conditions are true, and phaseToUse is omitted, the Charging Station / EVSE will make the selection on its own. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'startPeriod': start_period,
            'limit': limit
        }
        if number_phases is not None:
            temp_dict['numberPhases'] = number_phases
        if phase_to_use is not None:
            temp_dict['phaseToUse'] = phase_to_use
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_relative_time_interval(
        start: int,
        duration: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get relative time interval

        - Args: 
            - start(int): 
                - Relative_ Timer_ Interval. Start. Elapsed_ Time Start of the interval, in seconds from NOW. 
            - duration(int|None): 
                - Relative_ Timer_ Interval. Duration. Elapsed_ Time Duration of the interval, in seconds. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'start': start
        }
        if duration is not None:
            temp_dict['duration'] = duration
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_cost(
        cost_kind: str | CostKindType,
        amount: int,
        amount_multiplier: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get cost

        - Args: 
            - cost_kind(str): 
                - Cost. Cost_ Kind. Cost_ Kind_ Code The kind of cost referred to in the message element amount 
                - Enum: `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`
                - Or use EnumClass (Recommended): `CostKindType`. e.g. `CostKindType.carbon_dioxide_emission`
            - amount(int): 
                - Cost. Amount. Amount The estimated or actual cost per kWh 
            - amount_multiplier(int|None): 
                - Cost. Amount_ Multiplier. Integer Values: -3..3, The amountMultiplier defines the exponent to base 10 (dec). The final value is determined by: amount * 10 ^ amountMultiplier 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'costKind': cost_kind,
            'amount': amount
        }
        if amount_multiplier is not None:
            temp_dict['amountMultiplier'] = amount_multiplier
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_consumption_cost(
        start_value: int | float,
        cost: list,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get consumption cost

        - Args: 
            - start_value(int|float): 
                - Consumption_ Cost. Start_ Value. Numeric The lowest level of consumption that defines the starting point of this consumption block. The block interval extends to the start of the next interval. 
            - cost(list): 
                - Cost 
                - length limit: [1, 3]
                - recommended to use `get_cost()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'startValue': start_value,
            'cost': cost
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_sales_tariff_entry(
        relative_time_interval: dict,
        e_price_level: int | None = None,
        consumption_cost: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get sales tariff entry

        - Args: 
            - relative_time_interval(dict): 
                - Relative_ Timer_ Interval 
                - recommended to use `get_relative_time_interval()` to set element
            - e_price_level(int|None): 
                - Sales_ Tariff_ Entry. E_ Price_ Level. Unsigned_ Integer Defines the price level of this SalesTariffEntry (referring to NumEPriceLevels). Small values for the EPriceLevel represent a cheaper TariffEntry. Large values for the EPriceLevel represent a more expensive TariffEntry. 
            - consumption_cost(list|None): 
                - Consumption_ Cost 
                - length limit: [1, 3]
                - recommended to use `get_consumption_cost()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'relativeTimeInterval': relative_time_interval
        }
        if e_price_level is not None:
            temp_dict['ePriceLevel'] = e_price_level
        if consumption_cost is not None:
            temp_dict['consumptionCost'] = consumption_cost
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_sales_tariff(
        id: int,
        sales_tariff_entry: list,
        sales_tariff_description: str | None = None,
        num_eprice_levels: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get sales tariff

        - Args: 
            - id(int): 
                - Identified_ Object. MRID. Numeric_ Identifier SalesTariff identifier used to identify one sales tariff. An SAID remains a unique identifier for one schedule throughout a charging session. 
            - sales_tariff_entry(list): 
                - Sales_ Tariff_ Entry 
                - length limit: [1, 1024]
                - recommended to use `get_sales_tariff_entry()` to set element or to build a custom list.
            - sales_tariff_description(str|None): 
                - Sales_ Tariff. Sales. Tariff_ Description A human readable title/short description of the sales tariff e.g. for HMI display purposes. 
                - length limit: [1, 32]
            - num_eprice_levels(int|None): 
                - Sales_ Tariff. Num_ E_ Price_ Levels. Counter Defines the overall number of distinct price levels used across all provided SalesTariff elements. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id,
            'salesTariffEntry': sales_tariff_entry
        }
        if sales_tariff_description is not None:
            temp_dict['salesTariffDescription'] = sales_tariff_description
        if num_eprice_levels is not None:
            temp_dict['numEPriceLevels'] = num_eprice_levels
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_schedule(
        id: int,
        charging_rate_unit: str | ChargingRateUnitType,
        charging_schedule_period: list,
        start_schedule: str | None = None,
        duration: int | None = None,
        min_charging_rate: int | float | None = None,
        sales_tariff: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get charging schedule

        - Args: 
            - id(int): 
                - Identifies the ChargingSchedule. 
            - charging_rate_unit(str): 
                - Charging_ Schedule. Charging_ Rate_ Unit. Charging_ Rate_ Unit_ Code The unit of measure Limit is expressed in. 
                - Enum: `W`, `A`
                - Or use EnumClass (Recommended): `ChargingRateUnitType`. e.g. `ChargingRateUnitType.w`
            - charging_schedule_period(list): 
                - Charging_ Schedule_ Period Charging schedule period structure defines a time period in a charging schedule. 
                - length limit: [1, 1024]
                - recommended to use `get_charging_schedule_period()` to set element or to build a custom list.
            - start_schedule(str|None): 
                - Charging_ Schedule. Start_ Schedule. Date_ Time Starting point of an absolute schedule. If absent the schedule will be relative to start of charging. 
                - format: date-time
            - duration(int|None): 
                - Charging_ Schedule. Duration. Elapsed_ Time Duration of the charging schedule in seconds. If the duration is left empty, the last period will continue indefinitely or until end of the transaction if chargingProfilePurpose = TxProfile. 
            - min_charging_rate(int|float|None): 
                - Charging_ Schedule. Min_ Charging_ Rate. Numeric Minimum charging rate supported by the EV. The unit of measure is defined by the chargingRateUnit. This parameter is intended to be used by a local smart charging algorithm to optimize the power allocation for in the case a charging process is inefficient at lower charging rates. Accepts at most one digit fraction (e.g. 8.1) 
            - sales_tariff(dict|None): 
                - Sales_ Tariff NOTE: This dataType is based on dataTypes from <<ref-ISOIEC15118-2,ISO 15118-2>>. 
                - recommended to use `get_sales_tariff()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id,
            'chargingRateUnit': charging_rate_unit,
            'chargingSchedulePeriod': charging_schedule_period
        }
        if start_schedule is not None:
            temp_dict['startSchedule'] = start_schedule
        if duration is not None:
            temp_dict['duration'] = duration
        if min_charging_rate is not None:
            temp_dict['minChargingRate'] = min_charging_rate
        if sales_tariff is not None:
            temp_dict['salesTariff'] = sales_tariff
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_profile(
        id: int,
        stack_level: int,
        charging_profile_purpose: str | ChargingProfilePurposeType,
        charging_profile_kind: str | ChargingProfileKindType,
        charging_schedule: list,
        recurrency_kind: str | RecurrencyKindType | None = None,
        valid_from: str | None = None,
        valid_to: str | None = None,
        transaction_id: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get charging profile

        - Args: 
            - id(int): 
                - Identified_ Object. MRID. Numeric_ Identifier Id of ChargingProfile. 
            - stack_level(int): 
                - Charging_ Profile. Stack_ Level. Counter Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. 
            - charging_profile_purpose(str): 
                - Charging_ Profile. Charging_ Profile_ Purpose. Charging_ Profile_ Purpose_ Code Defines the purpose of the schedule transferred by this profile 
                - Enum: `ChargingStationExternalConstraints`, `ChargingStationMaxProfile`, `TxDefaultProfile`, `TxProfile`
                - Or use EnumClass (Recommended): `ChargingProfilePurposeType`. e.g. `ChargingProfilePurposeType.charging_station_external_constraints`
            - charging_profile_kind(str): 
                - Charging_ Profile. Charging_ Profile_ Kind. Charging_ Profile_ Kind_ Code Indicates the kind of schedule. 
                - Enum: `Absolute`, `Recurring`, `Relative`
                - Or use EnumClass (Recommended): `ChargingProfileKindType`. e.g. `ChargingProfileKindType.absolute`
            - charging_schedule(list): 
                - Charging_ Schedule Charging schedule structure defines a list of charging periods, as used in: GetCompositeSchedule.conf and ChargingProfile.  
                - length limit: [1, 3]
                - recommended to use `get_charging_schedule()` to set element or to build a custom list.
            - recurrency_kind(str||None): 
                - Charging_ Profile. Recurrency_ Kind. Recurrency_ Kind_ Code Indicates the start point of a recurrence. 
                - Enum: `Daily`, `Weekly`
                - Or use EnumClass (Recommended): `RecurrencyKindType`. e.g. `RecurrencyKindType.daily`
            - valid_from(str|None): 
                - Charging_ Profile. Valid_ From. Date_ Time Point in time at which the profile starts to be valid. If absent, the profile is valid as soon as it is received by the Charging Station. 
                - format: date-time
            - valid_to(str|None): 
                - Charging_ Profile. Valid_ To. Date_ Time Point in time at which the profile stops to be valid. If absent, the profile is valid until it is replaced by another profile. 
                - format: date-time
            - transaction_id(str|None): 
                - SHALL only be included if ChargingProfilePurpose is set to TxProfile. The transactionId is used to match the profile to a specific transaction. 
                - length limit: [1, 36]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id,
            'stackLevel': stack_level,
            'chargingProfilePurpose': charging_profile_purpose,
            'chargingProfileKind': charging_profile_kind,
            'chargingSchedule': charging_schedule
        }
        if recurrency_kind is not None:
            temp_dict['recurrencyKind'] = recurrency_kind
        if valid_from is not None:
            temp_dict['validFrom'] = valid_from
        if valid_to is not None:
            temp_dict['validTo'] = valid_to
        if transaction_id is not None:
            temp_dict['transactionId'] = transaction_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
