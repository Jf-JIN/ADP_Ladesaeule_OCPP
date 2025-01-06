from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_monitoring_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        seq_no: int,
        generated_at: str,
        monitor: list | None = None,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call.NotifyMonitoringReport:
        """
        Generate NotifyMonitoringReportRequest

        - Args: 
            - request_id(int): 
                - The id of the GetMonitoringRequest that requested this report. 
            - seq_no(int): 
                - Sequence number of this message. First message starts at 0. 
            - generated_at(str): 
                - Timestamp of the moment this message was generated at the Charging Station. 
                - format: date-time
            - monitor(list|None): 
                - Class to hold parameters of SetVariableMonitoring request. 
                - recommended to use `get_monitor()` to set element or to build a custom list.
            - tbc(bool|None): 
                - "to be continued" indicator. Indicates whether another part of the monitoringData follows in an upcoming notifyMonitoringReportRequest message. Default value when omitted is false. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.NotifyMonitoringReport
        """
        return call.NotifyMonitoringReport(
            request_id = request_id,
            seq_no = seq_no,
            generated_at = generated_at,
            monitor = monitor,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyMonitoringReport:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.NotifyMonitoringReport
        """
        return call.NotifyMonitoringReport(
            request_id = dict_data['requestId'],
            seq_no = dict_data['seqNo'],
            generated_at = dict_data['generatedAt'],
            monitor = dict_data.get('monitor', None),
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )


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
    def get_variable_monitoring(
        id: int,
        transaction: bool,
        value: int | float,
        type: str | MonitorType,
        severity: int,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get variable monitoring

        - Args: 
            - id(int): 
                - Identifies the monitor. 
            - transaction(bool): 
                - Monitor only active when a transaction is ongoing on a component relevant to this transaction.  
            - value(int|float): 
                - Value for threshold or delta monitoring. For Periodic or PeriodicClockAligned this is the interval in seconds. 
            - type(str): 
                - The type of this monitor, e.g. a threshold, delta or periodic monitor.  
                - Enum: `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`
                - Or use EnumClass (Recommended): `MonitorType`. e.g. `MonitorType.upper_threshold`
            - severity(int): 
                - The severity that will be assigned to an event that is triggered by this monitor. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event.  + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'id': id,
            'transaction': transaction,
            'value': value,
            'type': type,
            'severity': severity
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_monitor(
        component: dict,
        variable: dict,
        variable_monitoring: list,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get monitor

        - Args: 
            - component(dict): 
                - A physical or logical component 
                - recommended to use `get_component()` to set element
            - variable(dict): 
                - Reference key to a component-variable. 
                - recommended to use `get_variable()` to set element
            - variable_monitoring(list): 
                - A monitoring setting for a variable. 
                - recommended to use `get_variable_monitoring()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'component': component,
            'variable': variable,
            'variableMonitoring': variable_monitoring
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

