from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenAuthorizeResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id_tag_info: dict
    ) -> call_result.Authorize:
        """
        Generate AuthorizeResponse

        - Args: 
            - id_tag_info(dict): 
                - recommended to use `get_id_tag_info()` to set element

        - Returns:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_tag_info=id_tag_info
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Authorize:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_tag_info=dict_data['idTagInfo']
        )
