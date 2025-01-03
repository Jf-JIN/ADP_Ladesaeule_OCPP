
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, component_variable=None, component_criteria=None, custom_data=None) -> call.GetReport:
        """
        生成 GetReportRequest

        参数:
            -

        返回值:
            - call.GetReport
        """
        return call.GetReport(
            request_id = request_id,
            component_variable = component_variable,
            component_criteria = component_criteria,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetReport:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetReport
        """
        return call.GetReport(
            request_id = dict_data['requestId'],
            component_variable = dict_data.get('componentVariable', None),
            component_criteria = dict_data.get('componentCriteria', None),
            custom_data = dict_data.get('customData', None)
        )

