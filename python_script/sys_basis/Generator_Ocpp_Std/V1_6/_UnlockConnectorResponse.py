from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class unlock_connector_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | UnlockStatus
    ) -> call_result.UnlockConnector:
        """
        Generate UnlockConnectorResponse

        - Args: 
            - status(str|UnlockStatus): 
                - Enum: `Unlocked`, `UnlockFailed`, `NotSupported`
                - Or use EnumClass (Recommended): `UnlockStatus`. e.g. `UnlockStatus.unlocked`

        - Returns:
            - call_result.UnlockConnector
        """
        return call_result.UnlockConnector(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.UnlockConnector:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.UnlockConnector
        """
        return call_result.UnlockConnector(
            status = dict_data['status']
        )

