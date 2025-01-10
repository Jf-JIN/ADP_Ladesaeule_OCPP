from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenClearCacheResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ClearCacheStatus
    ) -> call_result.ClearCache:
        """
        Generate ClearCacheResponse

        - Args: 
            - status(str|ClearCacheStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `ClearCacheStatus`. e.g. `ClearCacheStatus.accepted`

        - Returns:
            - call_result.ClearCache
        """
        return call_result.ClearCache(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ClearCache:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ClearCache
        """
        return call_result.ClearCache(
            status=dict_data['status']
        )
