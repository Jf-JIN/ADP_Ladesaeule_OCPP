from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenSetMonitoringBaseRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        monitoring_base: str | MonitorBaseType,
        custom_data: dict | None = None
    ) -> call.SetMonitoringBase:
        """
        Generate SetMonitoringBaseRequest

        - Args: 
            - monitoring_base(str): 
                - Specify which monitoring base will be set 
                - Enum: `All`, `FactoryDefault`, `HardWiredOnly`
                - Or use EnumClass (Recommended): `MonitorBaseType`. e.g. `MonitorBaseType.all`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SetMonitoringBase
        """
        return call.SetMonitoringBase(
            monitoring_base=monitoring_base,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetMonitoringBase:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetMonitoringBase
        """
        return call.SetMonitoringBase(
            monitoring_base=dict_data['monitoringBase'],
            custom_data=dict_data.get('customData', None)
        )
