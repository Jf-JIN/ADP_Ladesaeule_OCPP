
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_variable_monitoring_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(set_monitoring_result, custom_data=None) -> call_result.SetVariableMonitoring:
        """
        生成 SetVariableMonitoringResponse

        参数:
            -

        返回值:
            - call_result.SetVariableMonitoring
        """
        return call_result.SetVariableMonitoring(
            set_monitoring_result = set_monitoring_result,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SetVariableMonitoring:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.SetVariableMonitoring
        """
        return call_result.SetVariableMonitoring(
            set_monitoring_result = dict_data['setMonitoringResult'],
            custom_data = dict_data.get('customData', None)
        )

