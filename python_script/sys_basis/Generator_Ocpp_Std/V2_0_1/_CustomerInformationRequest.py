from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenCustomerInformationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        request_id: int,
        report: bool,
        clear: bool,
        customer_certificate: dict | None = None,
        id_token: dict | None = None,
        customer_identifier: str | None = None,
        custom_data: dict | None = None
    ) -> call.CustomerInformation:
        """
        Generate CustomerInformationRequest

        - Args: 
            - request_id(int): 
                - The Id of the request. 
            - report(bool): 
                - Flag indicating whether the Charging Station should return NotifyCustomerInformationRequest messages containing information about the customer referred to. 
            - clear(bool): 
                - Flag indicating whether the Charging Station should clear all information about the customer referred to. 
            - customer_certificate(dict|None): 
                - recommended to use `get_customer_certificate()` to set element
            - id_token(dict|None): 
                - Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers. 
                - recommended to use `get_id_token()` to set element
            - customer_identifier(str|None): 
                - A (e.g. vendor specific) identifier of the customer this request refers to. This field contains a custom identifier other than IdToken and Certificate. One of the possible identifiers (customerIdentifier, customerIdToken or customerCertificate) should be in the request message. 
                - length limit: [1, 64]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            request_id=request_id,
            report=report,
            clear=clear,
            customer_certificate=customer_certificate,
            id_token=id_token,
            customer_identifier=customer_identifier,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CustomerInformation:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            request_id=dict_data['requestId'],
            report=dict_data['report'],
            clear=dict_data['clear'],
            customer_certificate=dict_data.get('customerCertificate', None),
            id_token=dict_data.get('idToken', None),
            customer_identifier=dict_data.get('customerIdentifier', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_customer_certificate(
        hash_algorithm: str | HashAlgorithmType,
        issuer_name_hash: str,
        issuer_key_hash: str,
        serial_number: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get customer certificate

        - Args: 
            - hash_algorithm(str): 
                - Used algorithms for the hashes provided. 
                - Enum: `SHA256`, `SHA384`, `SHA512`
                - Or use EnumClass (Recommended): `HashAlgorithmType`. e.g. `HashAlgorithmType.sha256`
            - issuer_name_hash(str): 
                - Hashed value of the Issuer DN (Distinguished Name). 
                - length limit: [1, 128]
            - issuer_key_hash(str): 
                - Hashed value of the issuers public key 
                - length limit: [1, 128]
            - serial_number(str): 
                - The serial number of the certificate. 
                - length limit: [1, 40]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'hashAlgorithm': hash_algorithm,
            'issuerNameHash': issuer_name_hash,
            'issuerKeyHash': issuer_key_hash,
            'serialNumber': serial_number
        }
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
