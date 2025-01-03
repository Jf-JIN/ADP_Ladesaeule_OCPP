
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_monitoring_report_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetMonitoringReport:
        """
        生成 GetMonitoringReportRequest

        参数:
            - 

        返回值:
            - call.GetMonitoringReport
        """
        return call.GetMonitoringReport(
            
        )

