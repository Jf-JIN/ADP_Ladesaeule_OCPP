
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_monitoring_report_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call.NotifyMonitoringReport:
        """
        生成 NotifyMonitoringReportRequest

        参数:
            - 

        返回值:
            - call.NotifyMonitoringReport
        """
        return call.NotifyMonitoringReport(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyMonitoringReport:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyMonitoringReport
        """
        return call.NotifyMonitoringReport(
            
        )

