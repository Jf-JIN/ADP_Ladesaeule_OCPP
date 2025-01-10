from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenGetConfigurationRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        key: list | None = None
    ) -> call.GetConfiguration:
        """
        Generate GetConfigurationRequest

        - Args: 
            - key(list|None): 
                - recommended to use `get_key()` to set element or to build a custom list.

        - Returns:
            - call.GetConfiguration
        """
        return call.GetConfiguration(
            key=key
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetConfiguration:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetConfiguration
        """
        return call.GetConfiguration(
            key=dict_data.get('key', None)
        )
