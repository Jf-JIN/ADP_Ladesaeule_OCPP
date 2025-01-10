from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenDeleteCertificateRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        certificate_hash_data: dict,
        custom_data: dict | None = None
    ) -> call.DeleteCertificate:
        """
        Generate DeleteCertificateRequest

        - Args: 
            - certificate_hash_data(dict): 
                - recommended to use `get_certificate_hash_data()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.DeleteCertificate
        """
        return call.DeleteCertificate(
            certificate_hash_data=certificate_hash_data,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.DeleteCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.DeleteCertificate
        """
        return call.DeleteCertificate(
            certificate_hash_data=dict_data['certificateHashData'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_certificate_hash_data(
        hash_algorithm: str | HashAlgorithmType,
        issuer_name_hash: str,
        issuer_key_hash: str,
        serial_number: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get certificate hash data

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
