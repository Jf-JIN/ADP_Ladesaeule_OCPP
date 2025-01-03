
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_charging_profiles_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, charging_profile, evse_id=None, custom_data=None) -> call.GetChargingProfiles:
        """
        生成 GetChargingProfilesRequest

        参数:
            -

        返回值:
            - call.GetChargingProfiles
        """
        return call.GetChargingProfiles(
            request_id = request_id,
            charging_profile = charging_profile,
            evse_id = evse_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetChargingProfiles:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetChargingProfiles
        """
        return call.GetChargingProfiles(
            request_id = dict_data['requestId'],
            charging_profile = dict_data['chargingProfile'],
            evse_id = dict_data.get('evseId', None),
            custom_data = dict_data.get('customData', None)
        )

