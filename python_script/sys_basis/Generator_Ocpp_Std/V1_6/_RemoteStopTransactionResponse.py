from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenRemoteStopTransactionResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | RemoteStartStopStatus
    ) -> call_result.RemoteStopTransaction:
        """
        Generate RemoteStopTransactionResponse

        - Args: 
            - status(str|RemoteStartStopStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `RemoteStartStopStatus`. e.g. `RemoteStartStopStatus.accepted`

        - Returns:
            - call_result.RemoteStopTransaction
        """
        return call_result.RemoteStopTransaction(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.RemoteStopTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.RemoteStopTransaction
        """
        return call_result.RemoteStopTransaction(
            status = dict_data['status']
        )

