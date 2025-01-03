
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_composite_schedule_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(status, connector_id=None, schedule_start=None, charging_schedule=None) -> call_result.GetCompositeSchedule:
        """
        生成 GetCompositeScheduleResponse

        参数:
            -

        返回值:
            - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            status = status,
            connector_id = connector_id,
            schedule_start = schedule_start,
            charging_schedule = charging_schedule
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetCompositeSchedule:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetCompositeSchedule
        """
        return call_result.GetCompositeSchedule(
            status = dict_data['status'],
            connector_id = dict_data.get('connectorId', None),
            schedule_start = dict_data.get('scheduleStart', None),
            charging_schedule = dict_data.get('chargingSchedule', None)
        )

