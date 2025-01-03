
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class boot_notification(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(charge_point_model, charge_point_vendor, charge_box_serial_number=None, charge_point_serial_number=None, firmware_version=None, iccid=None, imsi=None, meter_serial_number=None, meter_type=None) -> call.BootNotification:
        """
        生成 BootNotification

        参数:
            -

        返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charge_point_model = charge_point_model,
            charge_point_vendor = charge_point_vendor,
            charge_box_serial_number = charge_box_serial_number,
            charge_point_serial_number = charge_point_serial_number,
            firmware_version = firmware_version,
            iccid = iccid,
            imsi = imsi,
            meter_serial_number = meter_serial_number,
            meter_type = meter_type
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.BootNotification:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charge_point_model = dict_data['chargePointModel'],
            charge_point_vendor = dict_data['chargePointVendor'],
            charge_box_serial_number = dict_data.get('chargeBoxSerialNumber', None),
            charge_point_serial_number = dict_data.get('chargePointSerialNumber', None),
            firmware_version = dict_data.get('firmwareVersion', None),
            iccid = dict_data.get('iccid', None),
            imsi = dict_data.get('imsi', None),
            meter_serial_number = dict_data.get('meterSerialNumber', None),
            meter_type = dict_data.get('meterType', None)
        )

