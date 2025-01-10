from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenGetVariablesResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        get_variable_result: list,
        custom_data: dict | None = None
    ) -> call_result.GetVariables:
        """
        Generate GetVariablesResponse

        - Args: 
            - get_variable_result(list): 
                - Class to hold results of GetVariables request. 
                - recommended to use `get_get_variable_result()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetVariables
        """
        return call_result.GetVariables(
            get_variable_result=get_variable_result,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetVariables:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetVariables
        """
        return call_result.GetVariables(
            get_variable_result=dict_data['getVariableResult'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_attribute_status_info(
        reason_code: str,
        additional_info: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get attribute status info

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
        temp_dict: dict = {
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
        temp_dict: dict = {
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
        temp_dict: dict = {
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
        temp_dict: dict = {
            'name': name
        }
        if instance is not None:
            temp_dict['instance'] = instance
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_get_variable_result(
        attribute_status: str | GetVariableStatusType,
        component: dict,
        variable: dict,
        attribute_status_info: dict | None = None,
        attribute_type: str | AttributeType | None = None,
        attribute_value: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get variable result

        - Args: 
            - attribute_status(str): 
                - Result status of getting the variable. 
                - Enum: `Accepted`, `Rejected`, `UnknownComponent`, `UnknownVariable`, `NotSupportedAttributeType`
                - Or use EnumClass (Recommended): `GetVariableStatusType`. e.g. `GetVariableStatusType.accepted`
            - component(dict): 
                - A physical or logical component 
                - recommended to use `get_component()` to set element
            - variable(dict): 
                - Reference key to a component-variable. 
                - recommended to use `get_variable()` to set element
            - attribute_status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_attribute_status_info()` to set element
            - attribute_type(str||None): 
                - Attribute type for which value is requested. When absent, default Actual is assumed. 
                - Enum: `Actual`, `Target`, `MinSet`, `MaxSet`
                - Or use EnumClass (Recommended): `AttributeType`. e.g. `AttributeType.actual`
            - attribute_value(str|None): 
                - Value of requested attribute type of component-variable. This field can only be empty when the given status is NOT accepted. The Configuration Variable <<configkey-reporting-value-size,ReportingValueSize>> can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal.  
                - length limit: [1, 2500]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'attributeStatus': attribute_status,
            'component': component,
            'variable': variable
        }
        if attribute_status_info is not None:
            temp_dict['attributeStatusInfo'] = attribute_status_info
        if attribute_type is not None:
            temp_dict['attributeType'] = attribute_type
        if attribute_value is not None:
            temp_dict['attributeValue'] = attribute_value
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
