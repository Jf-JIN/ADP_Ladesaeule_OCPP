from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenResetResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ResetStatus
    ) -> call_result.Reset:
        """
        Generate ResetResponse

        - Args: 
            - status(str|ResetStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `ResetStatus`. e.g. `ResetStatus.accepted`

        - Returns:
            - call_result.Reset
        """
        return call_result.Reset(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Reset:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.Reset
        """
        return call_result.Reset(
            status = dict_data['status']
        )

