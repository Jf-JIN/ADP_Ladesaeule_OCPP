from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_event_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        generated_at: str,
        seq_no: int,
        event_data: list,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call.NotifyEvent:
        """
        Generate NotifyEventRequest

        - Args: 
            - generated_at(str): 
                - Timestamp of the moment this message was generated at the Charging Station. 
                - format: date-time
            - seq_no(int): 
                - Sequence number of this message. First message starts at 0. 
            - event_data(list): 
                - Class to report an event notification for a component-variable. 
                - recommended to use `get_event_data()` to set element or to build a custom list.
            - tbc(bool|None): 
                - “to be continued” indicator. Indicates whether another part of the report follows in an upcoming notifyEventRequest message. Default value when omitted is false.  
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.NotifyEvent
        """
        return call.NotifyEvent(
            generated_at = generated_at,
            seq_no = seq_no,
            event_data = event_data,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEvent:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.NotifyEvent
        """
        return call.NotifyEvent(
            generated_at = dict_data['generatedAt'],
            seq_no = dict_data['seqNo'],
            event_data = dict_data['eventData'],
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
    def get_event_data(
        event_id: int,
        timestamp: str,
        trigger: str | EventTriggerType,
        actual_value: str,
        component: dict,
        event_notification_type: str | EventNotificationType,
        variable: dict,
        cause: int | None = None,
        tech_code: str | None = None,
        tech_info: str | None = None,
        cleared: bool | None = None,
        transaction_id: str | None = None,
        variable_monitoring_id: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get event data

        - Args: 
            - event_id(int): 
                - Identifies the event. This field can be referred to as a cause by other events. 
            - timestamp(str): 
                - Timestamp of the moment the report was generated. 
                - format: date-time
            - trigger(str): 
                - Type of monitor that triggered this event, e.g. exceeding a threshold value. 
                - Enum: `Alerting`, `Delta`, `Periodic`
                - Or use EnumClass (Recommended): `EventTriggerType`. e.g. `EventTriggerType.alerting`
            - actual_value(str): 
                - Actual value (_attributeType_ Actual) of the variable. The Configuration Variable <<configkey-reporting-value-size,ReportingValueSize>> can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal.  
                - length limit: [1, 2500]
            - component(dict): 
                - A physical or logical component 
                - recommended to use `get_component()` to set element
            - event_notification_type(str): 
                - Specifies the event notification type of the message. 
                - Enum: `HardWiredNotification`, `HardWiredMonitor`, `PreconfiguredMonitor`, `CustomMonitor`
                - Or use EnumClass (Recommended): `EventNotificationType`. e.g. `EventNotificationType.hard_wired_notification`
            - variable(dict): 
                - Reference key to a component-variable. 
                - recommended to use `get_variable()` to set element
            - cause(int|None): 
                - Refers to the Id of an event that is considered to be the cause for this event. 
            - tech_code(str|None): 
                - Technical (error) code as reported by component. 
                - length limit: [1, 50]
            - tech_info(str|None): 
                - Technical detail information as reported by component. 
                - length limit: [1, 500]
            - cleared(bool|None): 
                - _Cleared_ is set to true to report the clearing of a monitored situation, i.e. a 'return to normal'.  
            - transaction_id(str|None): 
                - If an event notification is linked to a specific transaction, this field can be used to specify its transactionId. 
                - length limit: [1, 36]
            - variable_monitoring_id(int|None): 
                - Identifies the VariableMonitoring which triggered the event. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'eventId': event_id,
            'timestamp': timestamp,
            'trigger': trigger,
            'actualValue': actual_value,
            'component': component,
            'eventNotificationType': event_notification_type,
            'variable': variable
        }
        if cause is not None:
            temp_dict['cause'] = cause
        if tech_code is not None:
            temp_dict['techCode'] = tech_code
        if tech_info is not None:
            temp_dict['techInfo'] = tech_info
        if cleared is not None:
            temp_dict['cleared'] = cleared
        if transaction_id is not None:
            temp_dict['transactionId'] = transaction_id
        if variable_monitoring_id is not None:
            temp_dict['variableMonitoringId'] = variable_monitoring_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

