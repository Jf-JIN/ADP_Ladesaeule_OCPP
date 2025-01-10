from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenSetChargingProfileRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        cs_charging_profiles: dict
    ) -> call.SetChargingProfile:
        """
        Generate SetChargingProfileRequest

        - Args: 
            - connector_id(int): 
            - cs_charging_profiles(dict): 
                - recommended to use `get_cs_charging_profiles()` to set element

        - Returns:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id=connector_id,
            cs_charging_profiles=cs_charging_profiles
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            connector_id=dict_data['connectorId'],
            cs_charging_profiles=dict_data['csChargingProfiles']
        )
