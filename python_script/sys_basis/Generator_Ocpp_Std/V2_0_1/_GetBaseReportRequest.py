
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_base_report_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.GetBaseReport:
        """
        生成 GetBaseReportRequest

        参数:
        - 

        返回值:
        - call.GetBaseReport
        """
        return call.GetBaseReport(
            
        )

