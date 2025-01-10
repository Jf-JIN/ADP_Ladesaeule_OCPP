from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenChangeAvailabilityRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        operational_status: str | OperationalStatusType,
        evse: dict | None = None,
        custom_data: dict | None = None
    ) -> call.ChangeAvailability:
        """
        Generate ChangeAvailabilityRequest

        - Args: 
            - operational_status(str): 
                - This contains the type of availability change that the Charging Station should perform. 
                - Enum: `Inoperative`, `Operative`
                - Or use EnumClass (Recommended): `OperationalStatusType`. e.g. `OperationalStatusType.inoperative`
            - evse(dict|None): 
                - EVSE Electric Vehicle Supply Equipment 
                - recommended to use `get_evse()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            operational_status=operational_status,
            evse=evse,
            custom_data=custom_data
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
            operational_status=dict_data['operationalStatus'],
            evse=dict_data.get('evse', None),
            custom_data=dict_data.get('customData', None)
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
        temp_dict: dict = {
            'id': id
        }
        if connector_id is not None:
            temp_dict['connectorId'] = connector_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
