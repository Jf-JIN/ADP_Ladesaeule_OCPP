
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_report_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.NotifyReport:
        """
        生成 NotifyReportRequest

        参数:
        - 

        返回值:
        - call.NotifyReport
        """
        return call.NotifyReport(
            
        )

