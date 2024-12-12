
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_monitoring_report_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetMonitoringReport:
        """
        生成 GetMonitoringReportResponse

        参数:
        - 

        返回值:
        - call_result.GetMonitoringReport
        """
        return call_result.GetMonitoringReport(
            
        )

