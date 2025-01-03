
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_composite_schedule(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, duration, charging_rate_unit=None) -> call.GetCompositeSchedule:
        """
        生成 GetCompositeSchedule

        参数:
            -

        返回值:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            connector_id = connector_id,
            duration = duration,
            charging_rate_unit = charging_rate_unit
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetCompositeSchedule:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            connector_id = dict_data['connectorId'],
            duration = dict_data['duration'],
            charging_rate_unit = dict_data.get('chargingRateUnit', None)
        )

