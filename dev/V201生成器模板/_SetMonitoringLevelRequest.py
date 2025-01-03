
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_monitoring_level_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(severity, custom_data=None) -> call.SetMonitoringLevel:
        """
        生成 SetMonitoringLevelRequest

        参数:
            -

        返回值:
            - call.SetMonitoringLevel
        """
        return call.SetMonitoringLevel(
            severity = severity,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetMonitoringLevel:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetMonitoringLevel
        """
        return call.SetMonitoringLevel(
            severity = dict_data['severity'],
            custom_data = dict_data.get('customData', None)
        )

