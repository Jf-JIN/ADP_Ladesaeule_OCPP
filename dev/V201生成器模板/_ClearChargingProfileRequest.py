
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class clear_charging_profile_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(charging_profile_id=None, charging_profile_criteria=None, custom_data=None) -> call.ClearChargingProfile:
        """
        生成 ClearChargingProfileRequest

        参数:
            -

        返回值:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            charging_profile_id = charging_profile_id,
            charging_profile_criteria = charging_profile_criteria,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearChargingProfile:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            charging_profile_id = dict_data.get('chargingProfileId', None),
            charging_profile_criteria = dict_data.get('chargingProfileCriteria', None),
            custom_data = dict_data.get('customData', None)
        )

