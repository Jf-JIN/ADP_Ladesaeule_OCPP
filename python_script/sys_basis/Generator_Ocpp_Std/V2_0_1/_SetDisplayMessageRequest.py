from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_display_message_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        message: dict,
        custom_data: dict | None = None
    ) -> call.SetDisplayMessage:
        """
        Generate SetDisplayMessageRequest

        - Args: 
            - message(dict): 
                - Message_ Info Contains message details, for a message to be displayed on a Charging Station. 
                - recommended to use `get_message()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SetDisplayMessage
        """
        return call.SetDisplayMessage(
            message = message,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetDisplayMessage:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetDisplayMessage
        """
        return call.SetDisplayMessage(
            message = dict_data['message'],
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
    def get_display(
        name: str,
        evse: dict | None = None,
        instance: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get display

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
    def get_message(
        format: str | MessageFormatType,
        content: str,
        language: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get message

        - Args: 
            - format(str): 
                - Message_ Content. Format. Message_ Format_ Code Format of the message. 
                - Enum: `ASCII`, `HTML`, `URI`, `UTF8`
                - Or use EnumClass (Recommended): `MessageFormatType`. e.g. `MessageFormatType.ascii`
            - content(str): 
                - Message_ Content. Content. Message Message contents. 
                - length limit: [1, 512]
            - language(str|None): 
                - Message_ Content. Language. Language_ Code Message language identifier. Contains a language code as defined in <<ref-RFC5646,[RFC5646]>>. 
                - length limit: [1, 8]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'format': format,
            'content': content
        }
        if language is not None:
            temp_dict['language'] = language
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_message(
        id: int,
        priority: str | MessagePriorityType,
        message: dict,
        display: dict | None = None,
        state: str | MessageStateType | None = None,
        start_date_time: str | None = None,
        end_date_time: str | None = None,
        transaction_id: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get message

        - Args: 
            - id(int): 
                - Identified_ Object. MRID. Numeric_ Identifier Master resource identifier, unique within an exchange context. It is defined within the OCPP context as a positive Integer value (greater or equal to zero). 
            - priority(str): 
                - Message_ Info. Priority. Message_ Priority_ Code With what priority should this message be shown 
                - Enum: `AlwaysFront`, `InFront`, `NormalCycle`
                - Or use EnumClass (Recommended): `MessagePriorityType`. e.g. `MessagePriorityType.always_front`
            - message(dict): 
                - Message_ Content Contains message details, for a message to be displayed on a Charging Station. 
                - recommended to use `get_message()` to set element
            - display(dict|None): 
                - A physical or logical component 
                - recommended to use `get_display()` to set element
            - state(str||None): 
                - Message_ Info. State. Message_ State_ Code During what state should this message be shown. When omitted this message should be shown in any state of the Charging Station. 
                - Enum: `Charging`, `Faulted`, `Idle`, `Unavailable`
                - Or use EnumClass (Recommended): `MessageStateType`. e.g. `MessageStateType.charging`
            - start_date_time(str|None): 
                - Message_ Info. Start. Date_ Time From what date-time should this message be shown. If omitted: directly. 
                - format: date-time
            - end_date_time(str|None): 
                - Message_ Info. End. Date_ Time Until what date-time should this message be shown, after this date/time this message SHALL be removed. 
                - format: date-time
            - transaction_id(str|None): 
                - During which transaction shall this message be shown. Message SHALL be removed by the Charging Station after transaction has ended. 
                - length limit: [1, 36]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'id': id,
            'priority': priority,
            'message': message
        }
        if display is not None:
            temp_dict['display'] = display
        if state is not None:
            temp_dict['state'] = state
        if start_date_time is not None:
            temp_dict['startDateTime'] = start_date_time
        if end_date_time is not None:
            temp_dict['endDateTime'] = end_date_time
        if transaction_id is not None:
            temp_dict['transactionId'] = transaction_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

