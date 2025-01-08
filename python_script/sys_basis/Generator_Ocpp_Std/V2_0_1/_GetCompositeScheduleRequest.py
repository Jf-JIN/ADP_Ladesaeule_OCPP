from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_composite_schedule_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        duration: int,
        evse_id: int,
        charging_rate_unit: str | ChargingRateUnitType | None = None,
        custom_data: dict | None = None
    ) -> call.GetCompositeSchedule:
        """
        Generate GetCompositeScheduleRequest

        - Args: 
            - duration(int): 
                - Length of the requested schedule in seconds. 
            - evse_id(int): 
                - The ID of the EVSE for which the schedule is requested. When evseid=0, the Charging Station will calculate the expected consumption for the grid connection. 
            - charging_rate_unit(str||None): 
                - Can be used to force a power or current profile. 
                - Enum: `W`, `A`
                - Or use EnumClass (Recommended): `ChargingRateUnitType`. e.g. `ChargingRateUnitType.w`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetCompositeSchedule
        """
        return call.GetCompositeSchedule(
            duration = duration,
            evse_id = evse_id,
            charging_rate_unit = charging_rate_unit,
            custom_data = custom_data
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
            duration = dict_data['duration'],
            evse_id = dict_data['evseId'],
            charging_rate_unit = dict_data.get('chargingRateUnit', None),
            custom_data = dict_data.get('customData', None)
        )

