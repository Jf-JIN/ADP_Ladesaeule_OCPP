from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_configuration_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        configuration_key: list | None = None,
        unknown_key: list | None = None
    ) -> call_result.GetConfiguration:
        """
        Generate GetConfigurationResponse

        - Args: 
            - configuration_key(list|None): 
                - recommended to use `get_configuration_key()` to set element or to build a custom list.
            - unknown_key(list|None): 
                - recommended to use `get_unknown_key()` to set element or to build a custom list.

        - Returns:
            - call_result.GetConfiguration
        """
        return call_result.GetConfiguration(
            configuration_key = configuration_key,
            unknown_key = unknown_key
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetConfiguration:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetConfiguration
        """
        return call_result.GetConfiguration(
            configuration_key = dict_data.get('configurationKey', None),
            unknown_key = dict_data.get('unknownKey', None)
        )


    @staticmethod
    def get_configuration_key(
        key: str,
        readonly: bool,
        value: str | None = None
    ) -> dict:
        """
        Get configuration key

        - Args: 
            - key(str): 
                - length limit: [1, 50]
            - readonly(bool): 
            - value(str|None): 
                - length limit: [1, 500]

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'key': key,
            'readonly': readonly
        }
        if value is not None:
            temp_dict['value'] = value
        return temp_dict

