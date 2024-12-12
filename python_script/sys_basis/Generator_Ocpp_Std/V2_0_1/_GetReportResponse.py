
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_report_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.GetReport:
        """
        生成 GetReportResponse

        参数:
        - 

        返回值:
        - call_result.GetReport
        """
        return call_result.GetReport(
            
        )

