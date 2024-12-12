
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_monitoring_level_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetMonitoringLevel:
        """
        生成 SetMonitoringLevelRequest

        参数:
        - 

        返回值:
        - call.SetMonitoringLevel
        """
        return call.SetMonitoringLevel(
            
        )

