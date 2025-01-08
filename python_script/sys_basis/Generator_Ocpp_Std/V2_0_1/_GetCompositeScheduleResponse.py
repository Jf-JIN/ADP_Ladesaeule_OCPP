from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_composite_schedule_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | GenericStatusType,
        status_info: dict | None = None,
        schedule: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetCompositeSchedule:
        """
        Generate GetCompositeScheduleResponse

        - Args: 
            - status(str): 
                - The Charging Station will indicate if it was able to process the request 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `GenericStatusType`. e.g. `GenericStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - schedule(dict|None): 
                - Composite_ Schedule 
                - recommended to use `get_schedule()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            status = status,
            status_info = status_info,
            schedule = schedule,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetCompositeSchedule:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            status = dict_data['status'],
            status_info = dict_data.get('statusInfo', None),
            schedule = dict_data.get('schedule', None),
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
        temp_dict:dict = {
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
    def get_schedule(
        charging_schedule_period: list,
        evse_id: int,
        duration: int,
        schedule_start: str,
        charging_rate_unit: str | ChargingRateUnitType,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get schedule

        - Args: 
            - charging_schedule_period(list): 
                - Charging_ Schedule_ Period Charging schedule period structure defines a time period in a charging schedule. 
                - recommended to use `get_charging_schedule_period()` to set element or to build a custom list.
            - evse_id(int): 
                - The ID of the EVSE for which the schedule is requested. When evseid=0, the Charging Station calculated the expected consumption for the grid connection. 
            - duration(int): 
                - Duration of the schedule in seconds. 
            - schedule_start(str): 
                - Composite_ Schedule. Start. Date_ Time Date and time at which the schedule becomes active. All time measurements within the schedule are relative to this timestamp. 
                - format: date-time
            - charging_rate_unit(str): 
                - The unit of measure Limit is expressed in. 
                - Enum: `W`, `A`
                - Or use EnumClass (Recommended): `ChargingRateUnitType`. e.g. `ChargingRateUnitType.w`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'chargingSchedulePeriod': charging_schedule_period,
            'evseId': evse_id,
            'duration': duration,
            'scheduleStart': schedule_start,
            'chargingRateUnit': charging_rate_unit
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

