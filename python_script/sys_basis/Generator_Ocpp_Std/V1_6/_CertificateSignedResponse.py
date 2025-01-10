from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenCertificateSignedResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | CertificateSignedStatus
    ) -> call_result.CertificateSigned:
        """
        Generate CertificateSignedResponse

        - Args: 
            - status(str|CertificateSignedStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `CertificateSignedStatus`. e.g. `CertificateSignedStatus.accepted`

        - Returns:
            - call_result.CertificateSigned
        """
        return call_result.CertificateSigned(
            status=status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.CertificateSigned:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.CertificateSigned
        """
        return call_result.CertificateSigned(
            status=dict_data['status']
        )
