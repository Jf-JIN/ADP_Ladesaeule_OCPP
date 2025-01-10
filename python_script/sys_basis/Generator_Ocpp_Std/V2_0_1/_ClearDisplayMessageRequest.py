from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenClearDisplayMessageRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        id: int,
        custom_data: dict | None = None
    ) -> call.ClearDisplayMessage:
        """
        Generate ClearDisplayMessageRequest

        - Args: 
            - id(int): 
                - Id of the message that SHALL be removed from the Charging Station. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ClearDisplayMessage
        """
        return call.ClearDisplayMessage(
            id=id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearDisplayMessage:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ClearDisplayMessage
        """
        return call.ClearDisplayMessage(
            id=dict_data['id'],
            custom_data=dict_data.get('customData', None)
        )
