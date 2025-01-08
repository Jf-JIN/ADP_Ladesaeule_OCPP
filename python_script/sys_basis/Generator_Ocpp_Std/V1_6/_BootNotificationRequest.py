from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class boot_notification_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        charge_point_vendor: str,
        charge_point_model: str,
        charge_point_serial_number: str | None = None,
        charge_box_serial_number: str | None = None,
        firmware_version: str | None = None,
        iccid: str | None = None,
        imsi: str | None = None,
        meter_type: str | None = None,
        meter_serial_number: str | None = None
    ) -> call.BootNotification:
        """
        Generate BootNotificationRequest

        - Args: 
            - charge_point_vendor(str): 
                - length limit: [1, 20]
            - charge_point_model(str): 
                - length limit: [1, 20]
            - charge_point_serial_number(str|None): 
                - length limit: [1, 25]
            - charge_box_serial_number(str|None): 
                - length limit: [1, 25]
            - firmware_version(str|None): 
                - length limit: [1, 50]
            - iccid(str|None): 
                - length limit: [1, 20]
            - imsi(str|None): 
                - length limit: [1, 20]
            - meter_type(str|None): 
                - length limit: [1, 25]
            - meter_serial_number(str|None): 
                - length limit: [1, 25]

        - Returns:
            - call.BootNotification
        """
        return call.BootNotification(
            charge_point_vendor = charge_point_vendor,
            charge_point_model = charge_point_model,
            charge_point_serial_number = charge_point_serial_number,
            charge_box_serial_number = charge_box_serial_number,
            firmware_version = firmware_version,
            iccid = iccid,
            imsi = imsi,
            meter_type = meter_type,
            meter_serial_number = meter_serial_number
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.BootNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.BootNotification
        """
        return call.BootNotification(
            charge_point_vendor = dict_data['chargePointVendor'],
            charge_point_model = dict_data['chargePointModel'],
            charge_point_serial_number = dict_data.get('chargePointSerialNumber', None),
            charge_box_serial_number = dict_data.get('chargeBoxSerialNumber', None),
            firmware_version = dict_data.get('firmwareVersion', None),
            iccid = dict_data.get('iccid', None),
            imsi = dict_data.get('imsi', None),
            meter_type = dict_data.get('meterType', None),
            meter_serial_number = dict_data.get('meterSerialNumber', None)
        )

