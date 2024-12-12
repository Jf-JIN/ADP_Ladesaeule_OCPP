
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class notify_monitoring_report_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.NotifyMonitoringReport:
        """
        生成 NotifyMonitoringReportResponse

        参数:
        - 

        返回值:
        - call_result.NotifyMonitoringReport
        """
        return call_result.NotifyMonitoringReport(
            
        )

