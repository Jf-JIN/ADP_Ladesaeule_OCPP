
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class clear_variable_monitoring_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(clear_monitoring_result, custom_data=None) -> call_result.ClearVariableMonitoring:
        """
        生成 ClearVariableMonitoringResponse

        参数:
            -

        返回值:
            - call_result.ClearVariableMonitoring
        """
        return call_result.ClearVariableMonitoring(
            clear_monitoring_result = clear_monitoring_result,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearVariableMonitoring:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.ClearVariableMonitoring
        """
        return call_result.ClearVariableMonitoring(
            clear_monitoring_result = dict_data['clearMonitoringResult'],
            custom_data = dict_data.get('customData', None)
        )

