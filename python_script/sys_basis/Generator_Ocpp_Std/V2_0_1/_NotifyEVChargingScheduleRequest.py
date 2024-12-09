import jsonschema
from ocpp.v201 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class notify_ev_charging_schedule_request(Base_OCPP_Struct_V2_0_1):
    @staticmethod
    def generate(time_base: str, evse_id: int, charging_schedule: dict | None = None, custom_data: dict | None = None) -> call.NotifyEVChargingSchedule:
        """

        """
        temp_dict = {
            'timeBase': time_base,
            'evseId': evse_id,
            'chargingSchedule': charging_schedule
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data

        # try:  # 官方数据类是下划线表示法, 官方检查文件用的是小驼峰, 注意区别! (-.-")
        #     jsonschema.validate(temp_dict, STD_v2_0_1.NotifyEVChargingScheduleRequest)
        # except jsonschema.ValidationError as e:
        #     raise jsonschema.ValidationError(f"<notify_ev_charging_schedule_request> 生成器 错误: {e.message}")

        return call.NotifyEVChargingSchedule(
            time_base=time_base,
            evse_id=evse_id,
            charging_schedule=charging_schedule,
            custom_data=custom_data
        )


