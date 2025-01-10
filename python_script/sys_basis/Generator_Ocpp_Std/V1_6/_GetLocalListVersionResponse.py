from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenGetLocalListVersionResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        list_version: int
    ) -> call_result.GetLocalListVersion:
        """
        Generate GetLocalListVersionResponse

        - Args: 
            - list_version(int): 

        - Returns:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            list_version=list_version
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetLocalListVersion:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            list_version=dict_data['listVersion']
        )
