
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class set_charging_profile(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, cs_charging_profiles) -> call.SetChargingProfile:
        """
        生成 SetChargingProfile

        参数:
            -

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id = connector_id,
            cs_charging_profiles = cs_charging_profiles
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetChargingProfile:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id = dict_data['connectorId'],
            cs_charging_profiles = dict_data['csChargingProfiles']
        )

