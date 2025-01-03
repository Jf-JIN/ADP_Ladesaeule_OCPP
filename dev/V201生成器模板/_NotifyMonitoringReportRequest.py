
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_monitoring_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, seq_no, generated_at, monitor=None, tbc=None, custom_data=None) -> call.NotifyMonitoringReport:
        """
        生成 NotifyMonitoringReportRequest

        参数:
            -

        返回值:
            - call.NotifyMonitoringReport
        """
        return call.NotifyMonitoringReport(
            request_id = request_id,
            seq_no = seq_no,
            generated_at = generated_at,
            monitor = monitor,
            tbc = tbc,
            custom_data = custom_data
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
            request_id = dict_data['requestId'],
            seq_no = dict_data['seqNo'],
            generated_at = dict_data['generatedAt'],
            monitor = dict_data.get('monitor', None),
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

