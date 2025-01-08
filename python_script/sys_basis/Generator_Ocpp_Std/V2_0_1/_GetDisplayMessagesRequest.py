from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_display_messages_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        id: list | None = None,
        priority: str | MessagePriorityType | None = None,
        state: str | MessageStateType | None = None,
        custom_data: dict | None = None
    ) -> call.GetDisplayMessages:
        """
        Generate GetDisplayMessagesRequest

        - Args: 
            - request_id(int): 
                - The Id of this request. 
            - id(list|None): 
                - recommended to use `get_id()` to set element or to build a custom list.
            - priority(str||None): 
                - If provided the Charging Station shall return Display Messages with the given priority only. 
                - Enum: `AlwaysFront`, `InFront`, `NormalCycle`
                - Or use EnumClass (Recommended): `MessagePriorityType`. e.g. `MessagePriorityType.always_front`
            - state(str||None): 
                - If provided the Charging Station shall return Display Messages with the given state only.  
                - Enum: `Charging`, `Faulted`, `Idle`, `Unavailable`
                - Or use EnumClass (Recommended): `MessageStateType`. e.g. `MessageStateType.charging`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetDisplayMessages
        """
        return call.GetDisplayMessages(
            request_id = request_id,
            id = id,
            priority = priority,
            state = state,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetDisplayMessages:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetDisplayMessages
        """
        return call.GetDisplayMessages(
            request_id = dict_data['requestId'],
            id = dict_data.get('id', None),
            priority = dict_data.get('priority', None),
            state = dict_data.get('state', None),
            custom_data = dict_data.get('customData', None)
        )

