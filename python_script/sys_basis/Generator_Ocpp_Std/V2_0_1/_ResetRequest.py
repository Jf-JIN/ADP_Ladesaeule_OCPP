from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenResetRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        type: str | ResetType,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.Reset:
        """
        Generate ResetRequest

        - Args: 
            - type(str): 
                - This contains the type of reset that the Charging Station or EVSE should perform. 
                - Enum: `Immediate`, `OnIdle`
                - Or use EnumClass (Recommended): `ResetType`. e.g. `ResetType.immediate`
            - evse_id(int|None): 
                - This contains the ID of a specific EVSE that needs to be reset, instead of the entire Charging Station. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.Reset
        """
        return call.Reset(
            type=type,
            evse_id=evse_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Reset:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.Reset
        """
        return call.Reset(
            type=dict_data['type'],
            evse_id=dict_data.get('evseId', None),
            custom_data=dict_data.get('customData', None)
        )
