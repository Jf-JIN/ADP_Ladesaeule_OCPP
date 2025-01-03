
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class status_notification(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, error_code, status, timestamp=None, info=None, vendor_id=None, vendor_error_code=None) -> call.StatusNotification:
        """
        生成 StatusNotification

        参数:
            -

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            connector_id = connector_id,
            error_code = error_code,
            status = status,
            timestamp = timestamp,
            info = info,
            vendor_id = vendor_id,
            vendor_error_code = vendor_error_code
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StatusNotification:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.StatusNotification
        """
        return call.StatusNotification(
            connector_id = dict_data['connectorId'],
            error_code = dict_data['errorCode'],
            status = dict_data['status'],
            timestamp = dict_data.get('timestamp', None),
            info = dict_data.get('info', None),
            vendor_id = dict_data.get('vendorId', None),
            vendor_error_code = dict_data.get('vendorErrorCode', None)
        )

