
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class clear_variable_monitoring_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(**kwargs) -> call.ClearVariableMonitoring:
        """
        生成 ClearVariableMonitoringRequest

        参数:
            - 

        返回值:
            - call.ClearVariableMonitoring
        """
        return call.ClearVariableMonitoring(

        )
