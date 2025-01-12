from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenClearedChargingLimitRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        charging_limit_source: str | ChargingLimitSourceType,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.ClearedChargingLimit:
        """
        Generate ClearedChargingLimitRequest

        - Args: 
            - charging_limit_source(str): 
                - Source of the charging limit. 
                - Enum: `EMS`, `Other`, `SO`, `CSO`
                - Or use EnumClass (Recommended): `ChargingLimitSourceType`. e.g. `ChargingLimitSourceType.ems`
            - evse_id(int|None): 
                - EVSE Identifier. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ClearedChargingLimit
        """
        return call.ClearedChargingLimit(
            charging_limit_source=charging_limit_source,
            evse_id=evse_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearedChargingLimit:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ClearedChargingLimit
        """
        return call.ClearedChargingLimit(
            charging_limit_source=dict_data['chargingLimitSource'],
            evse_id=dict_data.get('evseId', None),
            custom_data=dict_data.get('customData', None)
        )
