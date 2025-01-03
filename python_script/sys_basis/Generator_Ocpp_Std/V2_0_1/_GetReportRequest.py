
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_report_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetReport:
        """
        生成 GetReportRequest

        参数:
            - 

        返回值:
            - call.GetReport
        """
        return call.GetReport(
            
        )

