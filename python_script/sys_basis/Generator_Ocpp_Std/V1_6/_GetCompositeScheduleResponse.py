from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenGetCompositeScheduleResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | GetCompositeScheduleStatus,
        connector_id: int | None = None,
        schedule_start: str | None = None,
        charging_schedule: dict | None = None
    ) -> call_result.GetCompositeSchedule:
        """
        Generate GetCompositeScheduleResponse

        - Args: 
            - status(str|GetCompositeScheduleStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `GetCompositeScheduleStatus`. e.g. `GetCompositeScheduleStatus.accepted`
            - connector_id(int|None): 
            - schedule_start(str|None): 
                - format: date-time
            - charging_schedule(dict|None): 
                - recommended to use `get_charging_schedule()` to set element

        - Returns:
            - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            status=status,
            connector_id=connector_id,
            schedule_start=schedule_start,
            charging_schedule=charging_schedule
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
            status=dict_data['status'],
            connector_id=dict_data.get('connectorId', None),
            schedule_start=dict_data.get('scheduleStart', None),
            charging_schedule=dict_data.get('chargingSchedule', None)
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
        charging_rate_unit: str | GetCompositeScheduleStatus,
        charging_schedule_period: list,
        duration: int | None = None,
        start_schedule: str | None = None,
        min_charging_rate: int | float | None = None
    ) -> dict:
        """
        Get charging schedule

        - Args: 
            - charging_rate_unit(str|GetCompositeScheduleStatus): 
                - Enum: `A`, `W`
                - Or use EnumClass (Recommended): `GetCompositeScheduleStatus`. e.g. `GetCompositeScheduleStatus.a`
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
