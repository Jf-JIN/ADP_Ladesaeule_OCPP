from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class change_configuration_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | ConfigurationStatus
    ) -> call_result.ChangeConfiguration:
        """
        Generate ChangeConfigurationResponse

        - Args: 
            - status(str|ConfigurationStatus): 
                - Enum: `Accepted`, `Rejected`, `RebootRequired`, `NotSupported`
                - Or use EnumClass (Recommended): `ConfigurationStatus`. e.g. `ConfigurationStatus.accepted`

        - Returns:
            - call_result.ChangeConfiguration
        """
        return call_result.ChangeConfiguration(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ChangeConfiguration:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ChangeConfiguration
        """
        return call_result.ChangeConfiguration(
            status = dict_data['status']
        )

