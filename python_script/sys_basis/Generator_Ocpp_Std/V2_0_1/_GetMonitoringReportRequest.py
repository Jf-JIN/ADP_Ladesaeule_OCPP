
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_monitoring_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, component_variable=None, monitoring_criteria=None, custom_data=None) -> call.GetMonitoringReport:
        """
        生成 GetMonitoringReportRequest

        参数:
            -

        返回值:
            - call.GetMonitoringReport
        """
        return call.GetMonitoringReport(
            request_id = request_id,
            component_variable = component_variable,
            monitoring_criteria = monitoring_criteria,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetMonitoringReport:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetMonitoringReport
        """
        return call.GetMonitoringReport(
            request_id = dict_data['requestId'],
            component_variable = dict_data.get('componentVariable', None),
            monitoring_criteria = dict_data.get('monitoringCriteria', None),
            custom_data = dict_data.get('customData', None)
        )

