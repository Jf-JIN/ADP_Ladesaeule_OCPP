
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, generated_at, seq_no, report_data=None, tbc=None, custom_data=None) -> call.NotifyReport:
        """
        生成 NotifyReportRequest

        参数:
            -

        返回值:
            - call.NotifyReport
        """
        return call.NotifyReport(
            request_id = request_id,
            generated_at = generated_at,
            seq_no = seq_no,
            report_data = report_data,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyReport:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyReport
        """
        return call.NotifyReport(
            request_id = dict_data['requestId'],
            generated_at = dict_data['generatedAt'],
            seq_no = dict_data['seqNo'],
            report_data = dict_data.get('reportData', None),
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

