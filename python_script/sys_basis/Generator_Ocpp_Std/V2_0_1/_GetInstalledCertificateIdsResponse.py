from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenGetInstalledCertificateIdsResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | GetInstalledCertificateStatusType,
        status_info: dict | None = None,
        certificate_hash_data_chain: list | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetInstalledCertificateIds:
        """
        Generate GetInstalledCertificateIdsResponse

        - Args: 
            - status(str): 
                - Charging Station indicates if it can process the request. 
                - Enum: `Accepted`, `NotFound`
                - Or use EnumClass (Recommended): `GetInstalledCertificateStatusType`. e.g. `GetInstalledCertificateStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - certificate_hash_data_chain(list|None): 
                - recommended to use `get_certificate_hash_data_chain()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            status=status,
            status_info=status_info,
            certificate_hash_data_chain=certificate_hash_data_chain,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetInstalledCertificateIds:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            status=dict_data['status'],
            status_info=dict_data.get('statusInfo', None),
            certificate_hash_data_chain=dict_data.get('certificateHashDataChain', None),
            custom_data=dict_data.get('customData', None)
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
        temp_dict: dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

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

    @staticmethod
    def get_child_certificate_hash_data(
        hash_algorithm: str | HashAlgorithmType,
        issuer_name_hash: str,
        issuer_key_hash: str,
        serial_number: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get child certificate hash data

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
    def get_certificate_hash_data_chain(
        certificate_hash_data: dict,
        certificate_type: str | GetCertificateIdUseType,
        child_certificate_hash_data: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get certificate hash data chain

        - Args: 
            - certificate_hash_data(dict): 
                - recommended to use `get_certificate_hash_data()` to set element
            - certificate_type(str): 
                - Indicates the type of the requested certificate(s). 
                - Enum: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `V2GCertificateChain`, `ManufacturerRootCertificate`
                - Or use EnumClass (Recommended): `GetCertificateIdUseType`. e.g. `GetCertificateIdUseType._v2g_root_certificate`
            - child_certificate_hash_data(list|None): 
                - length limit: [1, 4]
                - recommended to use `get_child_certificate_hash_data()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'certificateHashData': certificate_hash_data,
            'certificateType': certificate_type
        }
        if child_certificate_hash_data is not None:
            temp_dict['childCertificateHashData'] = child_certificate_hash_data
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
