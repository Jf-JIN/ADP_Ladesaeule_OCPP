from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenAuthorizeRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id_tag: str
    ) -> call.Authorize:
        """
        Generate AuthorizeRequest

        - Args: 
            - id_tag(str): 
                - length limit: [1, 20]

        - Returns:
            - call.Authorize
        """
        return call.Authorize(
            id_tag = id_tag
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Authorize:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.Authorize
        """
        return call.Authorize(
            id_tag = dict_data['idTag']
        )

