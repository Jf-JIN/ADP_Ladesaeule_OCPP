from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenClearCacheRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        
    ) -> call.ClearCache:
        """
        Generate ClearCacheRequest

        - Args: 
            

        - Returns:
            - call.ClearCache
        """
        return call.ClearCache(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearCache:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ClearCache
        """
        return call.ClearCache(
            
        )
