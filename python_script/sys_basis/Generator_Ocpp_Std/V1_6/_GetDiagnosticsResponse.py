from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class get_diagnostics_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        file_name: str | None = None
    ) -> call_result.GetDiagnostics:
        """
        Generate GetDiagnosticsResponse

        - Args: 
            - file_name(str|None): 
                - length limit: [1, 255]

        - Returns:
            - call_result.GetDiagnostics
        """
        return call_result.GetDiagnostics(
            file_name = file_name
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetDiagnostics:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetDiagnostics
        """
        return call_result.GetDiagnostics(
            file_name = dict_data.get('fileName', None)
        )

