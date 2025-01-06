from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_monitoring_level_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        severity: int,
        custom_data: dict | None = None
    ) -> call.SetMonitoringLevel:
        """
        Generate SetMonitoringLevelRequest

        - Args: 
            - severity(int): 
                - The Charging Station SHALL only report events with a severity number lower than or equal to this severity. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event.  + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations.  
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SetMonitoringLevel
        """
        return call.SetMonitoringLevel(
            severity = severity,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetMonitoringLevel:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetMonitoringLevel
        """
        return call.SetMonitoringLevel(
            severity = dict_data['severity'],
            custom_data = dict_data.get('customData', None)
        )

