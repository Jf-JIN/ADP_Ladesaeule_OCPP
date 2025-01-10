from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenGetBaseReportRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        report_base: str | ReportBaseType,
        custom_data: dict | None = None
    ) -> call.GetBaseReport:
        """
        Generate GetBaseReportRequest

        - Args: 
            - request_id(int): 
                - The Id of the request. 
            - report_base(str): 
                - This field specifies the report base. 
                - Enum: `ConfigurationInventory`, `FullInventory`, `SummaryInventory`
                - Or use EnumClass (Recommended): `ReportBaseType`. e.g. `ReportBaseType.configuration_inventory`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetBaseReport
        """
        return call.GetBaseReport(
            request_id=request_id,
            report_base=report_base,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetBaseReport:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetBaseReport
        """
        return call.GetBaseReport(
            request_id=dict_data['requestId'],
            report_base=dict_data['reportBase'],
            custom_data=dict_data.get('customData', None)
        )
