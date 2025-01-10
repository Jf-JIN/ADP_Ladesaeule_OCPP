from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenChangeAvailabilityRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        type: str | AvailabilityType
    ) -> call.ChangeAvailability:
        """
        Generate ChangeAvailabilityRequest

        - Args: 
            - connector_id(int): 
            - type(str|AvailabilityType): 
                - Enum: `Inoperative`, `Operative`
                - Or use EnumClass (Recommended): `AvailabilityType`. e.g. `AvailabilityType.inoperative`

        - Returns:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            connector_id = connector_id,
            type = type
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ChangeAvailability:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            connector_id = dict_data['connectorId'],
            type = dict_data['type']
        )

