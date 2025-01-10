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
