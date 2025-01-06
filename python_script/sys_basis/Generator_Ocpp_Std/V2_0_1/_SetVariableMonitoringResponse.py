from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class set_variable_monitoring_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        set_monitoring_result: list,
        custom_data: dict | None = None
    ) -> call_result.SetVariableMonitoring:
        """
        Generate SetVariableMonitoringResponse

        - Args: 
            - set_monitoring_result(list): 
                - Class to hold result of SetVariableMonitoring request. 
                - recommended to use `get_set_monitoring_result()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.SetVariableMonitoring
        """
        return call_result.SetVariableMonitoring(
            set_monitoring_result = set_monitoring_result,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SetVariableMonitoring:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SetVariableMonitoring
        """
        return call_result.SetVariableMonitoring(
            set_monitoring_result = dict_data['setMonitoringResult'],
            custom_data = dict_data.get('customData', None)
        )


    @staticmethod
    def get_status_info(
        reason_code: str,
        additional_info: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get status info

        - Args: 
            - reason_code(str): 
                - A predefined code for the reason why the status is returned in this response. The string is case-insensitive. 
                - length limit: [1, 20]
            - additional_info(str|None): 
                - Additional text to provide detailed information. 
                - length limit: [1, 512]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_evse(
        id: int,
        connector_id: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get evse

        - Args: 
            - id(int): 
                - Identified_ Object. MRID. Numeric_ Identifier EVSE Identifier. This contains a number (> 0) designating an EVSE of the Charging Station. 
            - connector_id(int|None): 
                - An id to designate a specific connector (on an EVSE) by connector index number. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'id': id
        }
        if connector_id is not None:
            temp_dict['connectorId'] = connector_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_component(
        name: str,
        evse: dict | None = None,
        instance: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get component

        - Args: 
            - name(str): 
                - Name of the component. Name should be taken from the list of standardized component names whenever possible. Case Insensitive. strongly advised to use Camel Case. 
                - length limit: [1, 50]
            - evse(dict|None): 
                - EVSE Electric Vehicle Supply Equipment 
                - recommended to use `get_evse()` to set element
            - instance(str|None): 
                - Name of instance in case the component exists as multiple instances. Case Insensitive. strongly advised to use Camel Case. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'name': name
        }
        if evse is not None:
            temp_dict['evse'] = evse
        if instance is not None:
            temp_dict['instance'] = instance
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_variable(
        name: str,
        instance: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get variable

        - Args: 
            - name(str): 
                - Name of the variable. Name should be taken from the list of standardized variable names whenever possible. Case Insensitive. strongly advised to use Camel Case. 
                - length limit: [1, 50]
            - instance(str|None): 
                - Name of instance in case the variable exists as multiple instances. Case Insensitive. strongly advised to use Camel Case. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'name': name
        }
        if instance is not None:
            temp_dict['instance'] = instance
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_set_monitoring_result(
        status: str | SetMonitoringStatusType,
        type: str | MonitorType,
        component: dict,
        variable: dict,
        severity: int,
        id: int | None = None,
        status_info: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get set monitoring result

        - Args: 
            - status(str): 
                - Status is OK if a value could be returned. Otherwise this will indicate the reason why a value could not be returned. 
                - Enum: `Accepted`, `UnknownComponent`, `UnknownVariable`, `UnsupportedMonitorType`, `Rejected`, `Duplicate`
                - Or use EnumClass (Recommended): `SetMonitoringStatusType`. e.g. `SetMonitoringStatusType.accepted`
            - type(str): 
                - The type of this monitor, e.g. a threshold, delta or periodic monitor.  
                - Enum: `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`
                - Or use EnumClass (Recommended): `MonitorType`. e.g. `MonitorType.upper_threshold`
            - component(dict): 
                - A physical or logical component 
                - recommended to use `get_component()` to set element
            - variable(dict): 
                - Reference key to a component-variable. 
                - recommended to use `get_variable()` to set element
            - severity(int): 
                - The severity that will be assigned to an event that is triggered by this monitor. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event.  + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. 
            - id(int|None): 
                - Id given to the VariableMonitor by the Charging Station. The Id is only returned when status is accepted. Installed VariableMonitors should have unique id's but the id's of removed Installed monitors should have unique id's but the id's of removed monitors MAY be reused. 
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'status': status,
            'type': type,
            'component': component,
            'variable': variable,
            'severity': severity
        }
        if id is not None:
            temp_dict['id'] = id
        if status_info is not None:
            temp_dict['statusInfo'] = status_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

