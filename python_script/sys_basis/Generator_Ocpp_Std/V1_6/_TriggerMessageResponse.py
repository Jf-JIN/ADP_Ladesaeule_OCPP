from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenTriggerMessageResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | TriggerMessageStatus
    ) -> call_result.TriggerMessage:
        """
        Generate TriggerMessageResponse

        - Args: 
            - status(str|TriggerMessageStatus): 
                - Enum: `Accepted`, `Rejected`, `NotImplemented`
                - Or use EnumClass (Recommended): `TriggerMessageStatus`. e.g. `TriggerMessageStatus.accepted`

        - Returns:
            - call_result.TriggerMessage
        """
        return call_result.TriggerMessage(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.TriggerMessage:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.TriggerMessage
        """
        return call_result.TriggerMessage(
            status=dict_data['status']
        )
