from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenTriggerMessageRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        requested_message: str | MessageTrigger,
        connector_id: int | None = None
    ) -> call.TriggerMessage:
        """
        Generate TriggerMessageRequest

        - Args: 
            - requested_message(str|MessageTrigger): 
                - Enum: `BootNotification`, `DiagnosticsStatusNotification`, `FirmwareStatusNotification`, `Heartbeat`, `MeterValues`, `StatusNotification`
                - Or use EnumClass (Recommended): `MessageTrigger`. e.g. `MessageTrigger.boot_notification`
            - connector_id(int|None): 

        - Returns:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = requested_message,
            connector_id = connector_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.TriggerMessage:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = dict_data['requestedMessage'],
            connector_id = dict_data.get('connectorId', None)
        )

