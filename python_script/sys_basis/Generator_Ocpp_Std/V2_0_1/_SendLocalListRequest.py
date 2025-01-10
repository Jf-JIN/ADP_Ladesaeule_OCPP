from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenSendLocalListRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        version_number: int,
        update_type: str | UpdateType,
        local_authorization_list: list | None = None,
        custom_data: dict | None = None
    ) -> call.SendLocalList:
        """
        Generate SendLocalListRequest

        - Args: 
            - version_number(int): 
                - In case of a full update this is the version number of the full list. In case of a differential update it is the version number of the list after the update has been applied. 
            - update_type(str): 
                - This contains the type of update (full or differential) of this request. 
                - Enum: `Differential`, `Full`
                - Or use EnumClass (Recommended): `UpdateType`. e.g. `UpdateType.differential`
            - local_authorization_list(list|None): 
                - Contains the identifier to use for authorization. 
                - recommended to use `get_local_authorization_list()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SendLocalList
        """
        return call.SendLocalList(
            version_number=version_number,
            update_type=update_type,
            local_authorization_list=local_authorization_list,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SendLocalList:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SendLocalList
        """
        return call.SendLocalList(
            version_number=dict_data['versionNumber'],
            update_type=dict_data['updateType'],
            local_authorization_list=dict_data.get('localAuthorizationList', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get additional info

        - Args: 
            - additional_id_token(str): 
                - This field specifies the additional IdToken. 
                - length limit: [1, 36]
            - type(str): 
                - This defines the type of the additionalIdToken. This is a custom type, so the implementation needs to be agreed upon by all involved parties. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get id token

        - Args: 
            - id_token(str): 
                - IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. 
                - length limit: [1, 36]
            - type(str): 
                - Enumeration of possible idToken types. 
                - Enum: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - Or use EnumClass (Recommended): `IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_additional_info()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get additional info

        - Args: 
            - additional_id_token(str): 
                - This field specifies the additional IdToken. 
                - length limit: [1, 36]
            - type(str): 
                - This defines the type of the additionalIdToken. This is a custom type, so the implementation needs to be agreed upon by all involved parties. 
                - length limit: [1, 50]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_group_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get group id token

        - Args: 
            - id_token(str): 
                - IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. 
                - length limit: [1, 36]
            - type(str): 
                - Enumeration of possible idToken types. 
                - Enum: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - Or use EnumClass (Recommended): `IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_additional_info()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_personal_message(
        format: str | MessageFormatType,
        content: str,
        language: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get personal message

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
        temp_dict: dict = {
            'format': format,
            'content': content
        }
        if language is not None:
            temp_dict['language'] = language
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_id_token_info(
        status: str | AuthorizationStatusType,
        cache_expiry_date_time: str | None = None,
        charging_priority: int | None = None,
        language1: str | None = None,
        evse_id: list | None = None,
        group_id_token: dict | None = None,
        language2: str | None = None,
        personal_message: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get id token info

        - Args: 
            - status(str): 
                - ID_ Token. Status. Authorization_ Status Current status of the ID Token. 
                - Enum: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`
                - Or use EnumClass (Recommended): `AuthorizationStatusType`. e.g. `AuthorizationStatusType.accepted`
            - cache_expiry_date_time(str|None): 
                - ID_ Token. Expiry. Date_ Time Date and Time after which the token must be considered invalid. 
                - format: date-time
            - charging_priority(int|None): 
                - Priority from a business point of view. Default priority is 0, The range is from -9 to 9. Higher values indicate a higher priority. The chargingPriority in <<transactioneventresponse,TransactionEventResponse>> overrules this one.  
            - language1(str|None): 
                - ID_ Token. Language1. Language_ Code Preferred user interface language of identifier user. Contains a language code as defined in <<ref-RFC5646,[RFC5646]>>. 
                - length limit: [1, 8]
            - evse_id(list|None): 
                - recommended to use `get_evse_id()` to set element or to build a custom list.
            - group_id_token(dict|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_group_id_token()` to set element
            - language2(str|None): 
                - ID_ Token. Language2. Language_ Code Second preferred user interface language of identifier user. Don't use when language1 is omitted, has to be different from language1. Contains a language code as defined in <<ref-RFC5646,[RFC5646]>>. 
                - length limit: [1, 8]
            - personal_message(dict|None): 
                - Message_ Content Contains message details, for a message to be displayed on a Charging Station. 
                - recommended to use `get_personal_message()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'status': status
        }
        if cache_expiry_date_time is not None:
            temp_dict['cacheExpiryDateTime'] = cache_expiry_date_time
        if charging_priority is not None:
            temp_dict['chargingPriority'] = charging_priority
        if language1 is not None:
            temp_dict['language1'] = language1
        if evse_id is not None:
            temp_dict['evseId'] = evse_id
        if group_id_token is not None:
            temp_dict['groupIdToken'] = group_id_token
        if language2 is not None:
            temp_dict['language2'] = language2
        if personal_message is not None:
            temp_dict['personalMessage'] = personal_message
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_local_authorization_list(
        id_token: dict,
        id_token_info: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get local authorization list

        - Args: 
            - id_token(dict): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_id_token()` to set element
            - id_token_info(dict|None): 
                - ID_ Token Contains status information about an identifier. It is advised to not stop charging for a token that expires during charging, as ExpiryDate is only used for caching purposes. If ExpiryDate is not given, the status has no end date. 
                - recommended to use `get_id_token_info()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token
        }
        if id_token_info is not None:
            temp_dict['idTokenInfo'] = id_token_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
