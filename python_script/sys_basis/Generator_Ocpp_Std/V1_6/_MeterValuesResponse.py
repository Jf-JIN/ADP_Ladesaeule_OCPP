from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenMeterValuesResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        
    ) -> call_result.MeterValues:
        """
        Generate MeterValuesResponse

        - Args: 
            

        - Returns:
            - call_result.MeterValues
        """
        return call_result.MeterValues(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.MeterValues:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.MeterValues
        """
        return call_result.MeterValues(
            
        )

