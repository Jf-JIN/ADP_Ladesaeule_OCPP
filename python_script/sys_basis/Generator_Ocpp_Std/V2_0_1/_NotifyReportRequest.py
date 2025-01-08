from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_report_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        generated_at: str,
        seq_no: int,
        report_data: list | None = None,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call.NotifyReport:
        """
        Generate NotifyReportRequest

        - Args: 
            - request_id(int): 
                - The id of the GetReportRequest  or GetBaseReportRequest that requested this report 
            - generated_at(str): 
                - Timestamp of the moment this message was generated at the Charging Station. 
                - format: date-time
            - seq_no(int): 
                - Sequence number of this message. First message starts at 0. 
            - report_data(list|None): 
                - Class to report components, variables and variable attributes and characteristics. 
                - recommended to use `get_report_data()` to set element or to build a custom list.
            - tbc(bool|None): 
                - "to be continued" indicator. Indicates whether another part of the report follows in an upcoming notifyReportRequest message. Default value when omitted is false. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.NotifyReport
        """
        return call.NotifyReport(
            request_id = request_id,
            generated_at = generated_at,
            seq_no = seq_no,
            report_data = report_data,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyReport:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.NotifyReport
        """
        return call.NotifyReport(
            request_id = dict_data['requestId'],
            generated_at = dict_data['generatedAt'],
            seq_no = dict_data['seqNo'],
            report_data = dict_data.get('reportData', None),
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
    def get_variable_attribute(
        type: str | AttributeType | None = None,
        value: str | None = None,
        mutability: str | MutabilityType | None = None,
        persistent: bool | None = None,
        constant: bool | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get variable attribute

        - Args: 
            - type(str||None): 
                - Attribute: Actual, MinSet, MaxSet, etc. Defaults to Actual if absent. 
                - Enum: `Actual`, `Target`, `MinSet`, `MaxSet`
                - Or use EnumClass (Recommended): `AttributeType`. e.g. `AttributeType.actual`
            - value(str|None): 
                - Value of the attribute. May only be omitted when mutability is set to 'WriteOnly'. The Configuration Variable <<configkey-reporting-value-size,ReportingValueSize>> can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal.  
                - length limit: [1, 2500]
            - mutability(str||None): 
                - Defines the mutability of this attribute. Default is ReadWrite when omitted. 
                - Enum: `ReadOnly`, `WriteOnly`, `ReadWrite`
                - Or use EnumClass (Recommended): `MutabilityType`. e.g. `MutabilityType.read_only`
            - persistent(bool|None): 
                - If true, value will be persistent across system reboots or power down. Default when omitted is false. 
            - constant(bool|None): 
                - If true, value that will never be changed by the Charging Station at runtime. Default when omitted is false. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            
        }
        if type is not None:
            temp_dict['type'] = type
        if value is not None:
            temp_dict['value'] = value
        if mutability is not None:
            temp_dict['mutability'] = mutability
        if persistent is not None:
            temp_dict['persistent'] = persistent
        if constant is not None:
            temp_dict['constant'] = constant
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_variable_characteristics(
        data_type: str | DataType,
        supports_monitoring: bool,
        unit: str | None = None,
        min_limit: int | float | None = None,
        max_limit: int | float | None = None,
        values_list: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get variable characteristics

        - Args: 
            - data_type(str): 
                - Data type of this variable. 
                - Enum: `string`, `decimal`, `integer`, `dateTime`, `boolean`, `OptionList`, `SequenceList`, `MemberList`
                - Or use EnumClass (Recommended): `DataType`. e.g. `DataType.string`
            - supports_monitoring(bool): 
                - Flag indicating if this variable supports monitoring.  
            - unit(str|None): 
                - Unit of the variable. When the transmitted value has a unit, this field SHALL be included. 
                - length limit: [1, 16]
            - min_limit(int|float|None): 
                - Minimum possible value of this variable. 
            - max_limit(int|float|None): 
                - Maximum possible value of this variable. When the datatype of this Variable is String, OptionList, SequenceList or MemberList, this field defines the maximum length of the (CSV) string. 
            - values_list(str|None): 
                - Allowed values when variable is Option/Member/SequenceList.  * OptionList: The (Actual) Variable value must be a single value from the reported (CSV) enumeration list. * MemberList: The (Actual) Variable value  may be an (unordered) (sub-)set of the reported (CSV) valid values list. * SequenceList: The (Actual) Variable value  may be an ordered (priority, etc)  (sub-)set of the reported (CSV) valid values. This is a comma separated list. The Configuration Variable <<configkey-configuration-value-size,ConfigurationValueSize>> can be used to limit SetVariableData.attributeValue and VariableCharacteristics.valueList. The max size of these values will always remain equal.  
                - length limit: [1, 1000]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'dataType': data_type,
            'supportsMonitoring': supports_monitoring
        }
        if unit is not None:
            temp_dict['unit'] = unit
        if min_limit is not None:
            temp_dict['minLimit'] = min_limit
        if max_limit is not None:
            temp_dict['maxLimit'] = max_limit
        if values_list is not None:
            temp_dict['valuesList'] = values_list
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_report_data(
        component: dict,
        variable: dict,
        variable_attribute: list,
        variable_characteristics: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get report data

        - Args: 
            - component(dict): 
                - A physical or logical component 
                - recommended to use `get_component()` to set element
            - variable(dict): 
                - Reference key to a component-variable. 
                - recommended to use `get_variable()` to set element
            - variable_attribute(list): 
                - Attribute data of a variable. 
                - length limit: [1, 4]
                - recommended to use `get_variable_attribute()` to set element or to build a custom list.
            - variable_characteristics(dict|None): 
                - Fixed read-only parameters of a variable. 
                - recommended to use `get_variable_characteristics()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'component': component,
            'variable': variable,
            'variableAttribute': variable_attribute
        }
        if variable_characteristics is not None:
            temp_dict['variableCharacteristics'] = variable_characteristics
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

