from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class reset_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        type: str | ResetType
    ) -> call.Reset:
        """
        Generate ResetRequest

        - Args: 
            - type(str|ResetType): 
                - Enum: `Hard`, `Soft`
                - Or use EnumClass (Recommended): `ResetType`. e.g. `ResetType.hard`

        - Returns:
            - call.Reset
        """
        return call.Reset(
            type = type
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
            type = dict_data['type']
        )

