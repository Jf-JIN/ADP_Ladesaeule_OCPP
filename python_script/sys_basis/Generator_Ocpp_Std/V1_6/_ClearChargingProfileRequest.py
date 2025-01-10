from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenClearChargingProfileRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id: int | None = None,
        connector_id: int | None = None,
        charging_profile_purpose: str | ChargingProfilePurposeType | None = None,
        stack_level: int | None = None
    ) -> call.ClearChargingProfile:
        """
        Generate ClearChargingProfileRequest

        - Args: 
            - id(int|None): 
            - connector_id(int|None): 
            - charging_profile_purpose(str|ChargingProfilePurposeType|None): 
                - Enum: `ChargePointMaxProfile`, `TxDefaultProfile`, `TxProfile`
                - Or use EnumClass (Recommended): `ChargingProfilePurposeType`. e.g. `ChargingProfilePurposeType.charge_point_max_profile`
            - stack_level(int|None): 

        - Returns:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            id=id,
            connector_id=connector_id,
            charging_profile_purpose=charging_profile_purpose,
            stack_level=stack_level
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearChargingProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ClearChargingProfile
        """
        return call.ClearChargingProfile(
            id=dict_data.get('id', None),
            connector_id=dict_data.get('connectorId', None),
            charging_profile_purpose=dict_data.get('chargingProfilePurpose', None),
            stack_level=dict_data.get('stackLevel', None)
        )
