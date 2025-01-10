from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenGetInstalledCertificateIdsResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | GetInstalledCertificateStatus,
        certificate_hash_data: list | None = None
    ) -> call_result.GetInstalledCertificateIds:
        """
        Generate GetInstalledCertificateIdsResponse

        - Args: 
            - status(str|GetInstalledCertificateStatus): 
                - Enum: `Accepted`, `NotFound`
                - Or use EnumClass (Recommended): `GetInstalledCertificateStatus`. e.g. `GetInstalledCertificateStatus.accepted`
            - certificate_hash_data(list|None): 
                - recommended to use `get_certificate_hash_data()` to set element or to build a custom list.

        - Returns:
            - call_result.GetInstalledCertificateIds
        """
        return call_result.GetInstalledCertificateIds(
            status = status,
            certificate_hash_data = certificate_hash_data
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
            status = dict_data['status'],
            certificate_hash_data = dict_data.get('certificateHashData', None)
        )


    @staticmethod
    def get_certificate_hash_data(
        hash_algorithm: str | HashAlgorithm,
        issuer_name_hash: str,
        issuer_key_hash: str,
        serial_number: str
    ) -> dict:
        """
        Get certificate hash data

        - Args: 
            - hash_algorithm(str|HashAlgorithm): 
                - Enum: `SHA256`, `SHA384`, `SHA512`
                - Or use EnumClass (Recommended): `HashAlgorithm`. e.g. `HashAlgorithm.sha256`
            - issuer_name_hash(str): 
                - length limit: [1, 128]
            - issuer_key_hash(str): 
                - length limit: [1, 128]
            - serial_number(str): 
                - length limit: [1, 40]

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'hashAlgorithm': hash_algorithm,
            'issuerNameHash': issuer_name_hash,
            'issuerKeyHash': issuer_key_hash,
            'serialNumber': serial_number
        }
        return temp_dict

