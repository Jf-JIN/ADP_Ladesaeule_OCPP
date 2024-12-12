
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class clear_variable_monitoring_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.ClearVariableMonitoring:
        """
        生成 ClearVariableMonitoringResponse

        参数:
        - 

        返回值:
        - call_result.ClearVariableMonitoring
        """
        return call_result.ClearVariableMonitoring(
            
        )

