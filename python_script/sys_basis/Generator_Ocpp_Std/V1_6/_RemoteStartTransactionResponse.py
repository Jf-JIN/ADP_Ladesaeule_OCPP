from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class remote_start_transaction_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | RemoteStartStopStatus
    ) -> call_result.RemoteStartTransaction:
        """
        Generate RemoteStartTransactionResponse

        - Args: 
            - status(str|RemoteStartStopStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `RemoteStartStopStatus`. e.g. `RemoteStartStopStatus.accepted`

        - Returns:
            - call_result.RemoteStartTransaction
        """
        return call_result.RemoteStartTransaction(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.RemoteStartTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.RemoteStartTransaction
        """
        return call_result.RemoteStartTransaction(
            status = dict_data['status']
        )

