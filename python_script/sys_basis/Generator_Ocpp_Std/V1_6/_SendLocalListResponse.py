from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenSendLocalListResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | UpdateStatus
    ) -> call_result.SendLocalList:
        """
        Generate SendLocalListResponse

        - Args: 
            - status(str|UpdateStatus): 
                - Enum: `Accepted`, `Failed`, `NotSupported`, `VersionMismatch`
                - Or use EnumClass (Recommended): `UpdateStatus`. e.g. `UpdateStatus.accepted`

        - Returns:
            - call_result.SendLocalList
        """
        return call_result.SendLocalList(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SendLocalList:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SendLocalList
        """
        return call_result.SendLocalList(
            status=dict_data['status']
        )
