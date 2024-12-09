
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class notify_ev_charging_schedule_request(Base_OCPP_Struct_V2_0_1):
    @staticmethod
    def generate(time_base: str, evse_id: int, charging_schedule: dict | None = None, custom_data: dict | None = None, **kwargs) -> call.NotifyEVChargingSchedule:
        """
        生成 NotifyEVChargingScheduleRequest

        参数:
        - 

        返回值:
        - call_result.NotifyEVChargingSchedule
        """

        return call.NotifyEVChargingSchedule(
            time_base=time_base or kwargs.get('time_base', None),
            evse_id=evse_id or kwargs.get('evse_id', None),
            charging_schedule=charging_schedule or kwargs.get('charging_schedule', None),
            custom_data=custom_data or kwargs.get('custom_data', None)
        )
