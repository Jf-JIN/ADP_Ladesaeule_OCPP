from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenReserveNowRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        id: int,
        expiry_date_time: str,
        id_token: dict,
        connector_type: str | ConnectorType | None = None,
        evse_id: int | None = None,
        group_id_token: dict | None = None,
        custom_data: dict | None = None
    ) -> call.ReserveNow:
        """
        Generate ReserveNowRequest

        - Args: 
            - id(int): 
                - Id of reservation. 
            - expiry_date_time(str): 
                - Date and time at which the reservation expires. 
                - format: date-time
            - id_token(dict): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_id_token()` to set element
            - connector_type(str||None): 
                - This field specifies the connector type. 
                - Enum: `cCCS1`, `cCCS2`, `cG105`, `cTesla`, `cType1`, `cType2`, `s309-1P-16A`, `s309-1P-32A`, `s309-3P-16A`, `s309-3P-32A`, `sBS1361`, `sCEE-7-7`, `sType2`, `sType3`, `Other1PhMax16A`, `Other1PhOver16A`, `Other3Ph`, `Pan`, `wInductive`, `wResonant`, `Undetermined`, `Unknown`
                - Or use EnumClass (Recommended): `ConnectorType`. e.g. `ConnectorType.c_ccs1`
            - evse_id(int|None): 
                - This contains ID of the evse to be reserved. 
            - group_id_token(dict|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_group_id_token()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.ReserveNow
        """
        return call.ReserveNow(
            id=id,
            expiry_date_time=expiry_date_time,
            id_token=id_token,
            connector_type=connector_type,
            evse_id=evse_id,
            group_id_token=group_id_token,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReserveNow:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.ReserveNow
        """
        return call.ReserveNow(
            id=dict_data['id'],
            expiry_date_time=dict_data['expiryDateTime'],
            id_token=dict_data['idToken'],
            connector_type=dict_data.get('connectorType', None),
            evse_id=dict_data.get('evseId', None),
            group_id_token=dict_data.get('groupIdToken', None),
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
