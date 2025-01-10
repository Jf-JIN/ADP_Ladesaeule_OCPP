from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenGetLogResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | LogStatus,
        filename: str | None = None
    ) -> call_result.GetLog:
        """
        Generate GetLogResponse

        - Args: 
            - status(str|LogStatus): 
                - Enum: `Accepted`, `Rejected`, `AcceptedCanceled`
                - Or use EnumClass (Recommended): `LogStatus`. e.g. `LogStatus.accepted`
            - filename(str|None): 
                - length limit: [1, 255]

        - Returns:
            - call_result.GetLog
        """
        return call_result.GetLog(
            status = status,
            filename = filename
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetLog:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetLog
        """
        return call_result.GetLog(
            status = dict_data['status'],
            filename = dict_data.get('filename', None)
        )

