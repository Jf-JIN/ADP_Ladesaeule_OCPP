from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class trigger_message_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        requested_message: str | MessageTriggerType,
        evse: dict | None = None,
        custom_data: dict | None = None
    ) -> call.TriggerMessage:
        """
        Generate TriggerMessageRequest

        - Args: 
            - requested_message(str): 
                - Type of message to be triggered. 
                - Enum: `BootNotification`, `LogStatusNotification`, `FirmwareStatusNotification`, `Heartbeat`, `MeterValues`, `SignChargingStationCertificate`, `SignV2GCertificate`, `StatusNotification`, `TransactionEvent`, `SignCombinedCertificate`, `PublishFirmwareStatusNotification`
                - Or use EnumClass (Recommended): `MessageTriggerType`. e.g. `MessageTriggerType.boot_notification`
            - evse(dict|None): 
                - EVSE Electric Vehicle Supply Equipment 
                - recommended to use `get_evse()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.TriggerMessage
        """
        return call.TriggerMessage(
            requested_message = requested_message,
            evse = evse,
            custom_data = custom_data
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
            evse = dict_data.get('evse', None),
            custom_data = dict_data.get('customData', None)
        )


    @staticmethod
    def get_evse(
        id: int,
        connector_id: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get evse

        - Args: 
            - id(int): 
                - Identified_ Object. MRID. Numeric_ Identifier EVSE Identifier. This contains a number (> 0) designating an EVSE of the Charging Station. 
            - connector_id(int|None): 
                - An id to designate a specific connector (on an EVSE) by connector index number. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'id': id
        }
        if connector_id is not None:
            temp_dict['connectorId'] = connector_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

