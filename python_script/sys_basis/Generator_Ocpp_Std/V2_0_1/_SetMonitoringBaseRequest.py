
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_monitoring_base_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.SetMonitoringBase:
        """
        生成 SetMonitoringBaseRequest

        参数:
        - 

        返回值:
        - call.SetMonitoringBase
        """
        return call.SetMonitoringBase(
            
        )

