from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenReportChargingProfilesResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        custom_data: dict | None = None
    ) -> call_result.ReportChargingProfiles:
        """
        Generate ReportChargingProfilesResponse

        - Args: 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.ReportChargingProfiles
        """
        return call_result.ReportChargingProfiles(
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.ReportChargingProfiles:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.ReportChargingProfiles
        """
        return call_result.ReportChargingProfiles(
            custom_data=dict_data.get('customData', None)
        )
