from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenGetCompositeScheduleRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        duration: int,
        charging_rate_unit: str | ChargingRateUnitType | None = None
    ) -> call.GetCompositeSchedule:
        """
        Generate GetCompositeScheduleRequest

        - Args: 
            - connector_id(int): 
            - duration(int): 
            - charging_rate_unit(str|ChargingRateUnitType|None): 
                - Enum: `A`, `W`
                - Or use EnumClass (Recommended): `ChargingRateUnitType`. e.g. `ChargingRateUnitType.a`

        - Returns:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            connector_id = connector_id,
            duration = duration,
            charging_rate_unit = charging_rate_unit
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetCompositeSchedule:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            connector_id = dict_data['connectorId'],
            duration = dict_data['duration'],
            charging_rate_unit = dict_data.get('chargingRateUnit', None)
        )

