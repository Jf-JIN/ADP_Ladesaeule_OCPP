
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_variable_monitoring_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SetVariableMonitoring:
        """
        生成 SetVariableMonitoringResponse

        参数:
        - 

        返回值:
        - call_result.SetVariableMonitoring
        """
        return call_result.SetVariableMonitoring(
            
        )

