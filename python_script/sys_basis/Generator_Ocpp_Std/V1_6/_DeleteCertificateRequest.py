from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class delete_certificate_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        certificate_hash_data: dict
    ) -> call.DeleteCertificate:
        """
        Generate DeleteCertificateRequest

        - Args: 
            - certificate_hash_data(dict): 
                - recommended to use `get_certificate_hash_data()` to set element

        - Returns:
            - call.DeleteCertificate
        """
        return call.DeleteCertificate(
            certificate_hash_data = certificate_hash_data
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
            certificate_hash_data = dict_data['certificateHashData']
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

