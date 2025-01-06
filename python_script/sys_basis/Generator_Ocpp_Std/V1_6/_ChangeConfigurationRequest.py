from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class change_configuration_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        key: str,
        value: str
    ) -> call.ChangeConfiguration:
        """
        Generate ChangeConfigurationRequest

        - Args: 
            - key(str): 
                - length limit: [1, 50]
            - value(str): 
                - length limit: [1, 500]

        - Returns:
            - call.ChangeConfiguration
        """
        return call.ChangeConfiguration(
            key = key,
            value = value
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ChangeConfiguration:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ChangeConfiguration
        """
        return call.ChangeConfiguration(
            key = dict_data['key'],
            value = dict_data['value']
        )

