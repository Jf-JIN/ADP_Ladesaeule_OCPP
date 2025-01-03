
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class clear_variable_monitoring_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id, custom_data=None) -> call.ClearVariableMonitoring:
        """
        生成 ClearVariableMonitoringRequest

        参数:
            -

        返回值:
            - call.ClearVariableMonitoring
        """
        return call.ClearVariableMonitoring(
            id = id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearVariableMonitoring:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ClearVariableMonitoring
        """
        return call.ClearVariableMonitoring(
            id = dict_data['id'],
            custom_data = dict_data.get('customData', None)
        )

