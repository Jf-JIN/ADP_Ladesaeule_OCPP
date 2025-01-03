
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_log_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(log, log_type, request_id, retries=None, retry_interval=None, custom_data=None) -> call.GetLog:
        """
        生成 GetLogRequest

        参数:
            -

        返回值:
            - call.GetLog
        """
        return call.GetLog(
            log = log,
            log_type = log_type,
            request_id = request_id,
            retries = retries,
            retry_interval = retry_interval,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetLog:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetLog
        """
        return call.GetLog(
            log = dict_data['log'],
            log_type = dict_data['logType'],
            request_id = dict_data['requestId'],
            retries = dict_data.get('retries', None),
            retry_interval = dict_data.get('retryInterval', None),
            custom_data = dict_data.get('customData', None)
        )

