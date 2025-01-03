
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_charging_profile_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(evse_id, charging_profile, custom_data=None) -> call.SetChargingProfile:
        """
        生成 SetChargingProfileRequest

        参数:
            -

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            evse_id = evse_id,
            charging_profile = charging_profile,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetChargingProfile:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            evse_id = dict_data['evseId'],
            charging_profile = dict_data['chargingProfile'],
            custom_data = dict_data.get('customData', None)
        )

