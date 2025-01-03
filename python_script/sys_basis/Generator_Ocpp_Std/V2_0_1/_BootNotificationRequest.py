
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class boot_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        charging_station: dict,
        reason: str | BootReasonType,
        custom_data: dict | None = None,
        **kwargs
    ) -> call.BootNotification:
        """
        生成 BootNotificationRequest

        参数:
            - charging_station(dict): 充电站, 推荐使用`get_charging_station()`传入
            - reason(str|BootReasonType): 类型, 候选: 
                - `ApplicationReset`, `FirmwareUpdate`, `LocalReset`, `PowerUp`, `RemoteReset`, `ScheduledReset`, `Triggered`, `Unknown`, `Watchdog`.
                - 或者可以使用 `BootReasonType` 枚举, 例如: `BootReasonType.firmware_update` .
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charging_station=charging_station or kwargs["chargingStation"],
            reason=reason or kwargs["reason"],
            custom_data=custom_data or kwargs.get("customData", None)
        )

    @staticmethod
    def get_charging_station(
        model: str,
        vendor_name: str,
        serial_number: str | None = None,
        firmware_version: str | None = None,
        modem: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 charging_station(dict)

        参数:
            - model(str): 设备型号, 长度为[1-20] 个字符
            - vendor_name(str): 标识供应商, 长度为[1-50] 个字符
            - serial_number(str): 设备序列号, 长度为[1-25] 个字符
            - firmware_version(str): 包含充电站的固件版本, 长度为[1-50] 个字符
            - modem(dict): 推荐使用 `get_modem()` 传入
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - charging_station(dict)
        """

        temp_dict = {
            "model": model,
            "vendorName": vendor_name
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if serial_number is not None:
            temp_dict["serialNumber"] = serial_number
        if modem is not None:
            temp_dict["modem"] = modem
        if firmware_version is not None:
            temp_dict["firmwareVersion"] = firmware_version
        return temp_dict

    @staticmethod
    def get_modem(iccid: str | None = None, imsi: str | None = None, custom_data: dict | None = None) -> dict:
        """
        生成 modem(dict)

        参数:
            - iccid(str): 无线通信模块ICCID, 长度为[1-20] 个字符
            - imsi(str): 无线通信模块IMSI, 长度为[1-20] 个字符
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - modem(dict)
        """
        temp_dict = {
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if iccid is not None:
            temp_dict["iccid"] = iccid
        if imsi is not None:
            temp_dict["imsi"] = imsi
        return temp_dict
