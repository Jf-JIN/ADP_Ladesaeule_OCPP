
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_monitoring_base_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.SetMonitoringBase:
        """
        生成 SetMonitoringBaseResponse

        参数:
        - 

        返回值:
        - call_result.SetMonitoringBase
        """
        return call_result.SetMonitoringBase(
            
        )

