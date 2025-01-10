from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenBootNotificationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        charging_station: dict,
        reason: str | BootReasonType,
        custom_data: dict | None = None
    ) -> call.BootNotification:
        """
        生成 BootNotificationRequest

        - 参数: 
            - charging_station(dict): 
                - Charge_ Point 可以为电动汽车 (EV) 充电的物理系统. 
                - 推荐使用 `get_charging_station()` 传入
            - reason(str): 
                - 这包含将此消息发送到 CSMS 的原因. 
                - 枚举值: `ApplicationReset`, `FirmwareUpdate`, `LocalReset`, `PowerUp`, `RemoteReset`, `ScheduledReset`, `Triggered`, `Unknown`, `Watchdog`
                - 或使用枚举类(推荐)`BootReasonType`. e.g. `BootReasonType.application_reset`
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charging_station=charging_station,
            reason=reason,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.BootNotification:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.BootNotification
        """
        return call.BootNotification(
            charging_station=dict_data['chargingStation'],
            reason=dict_data['reason'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_modem(
        iccid: str | None = None,
        imsi: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 modem

        - 参数: 
            - iccid(str|None): 
                - 无线通信模块ICCID. CI20_ Text 包含调制解调器 SIM 卡的 ICCID. 
                - 长度范围: [1, 20]
            - imsi(str|None): 
                - 无线通信模块IMSI. 国际移动用户识别码. CI20_ Text 包含调制解调器 SIM 卡的 IMSI. 
                - 长度范围: [1, 20]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {

        }
        if iccid is not None:
            temp_dict['iccid'] = iccid
        if imsi is not None:
            temp_dict['imsi'] = imsi
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_station(
        model: str,
        vendor_name: str,
        serial_number: str | None = None,
        modem: dict | None = None,
        firmware_version: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 charging station

        - 参数: 
            - model(str): 
                - 设备型号. CI20_ Text 定义设备型号. 
                - 长度范围: [1, 20]
            - vendor_name(str): 
                - 供应商标识(不一定以独特的方式). 
                - 长度范围: [1, 50]
            - serial_number(str|None): 
                - 设备序列号. Serial_ Number 供应商特定的设备标识符.
                - 长度范围: [1, 25]
            - modem(dict|None): 
                - 无线通信模块 定义启动和维持与其他设备的无线通信所需的参数. 
                - 推荐使用 `get_modem()` 传入
            - firmware_version(str|None): 
                - 其中包含充电站的固件版本. 
                - 长度范围: [1, 50]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'model': model,
            'vendorName': vendor_name
        }
        if serial_number is not None:
            temp_dict['serialNumber'] = serial_number
        if modem is not None:
            temp_dict['modem'] = modem
        if firmware_version is not None:
            temp_dict['firmwareVersion'] = firmware_version
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
