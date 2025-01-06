from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class install_certificate_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | CertificateStatus
    ) -> call_result.InstallCertificate:
        """
        Generate InstallCertificateResponse

        - Args: 
            - status(str|CertificateStatus): 
                - Enum: `Accepted`, `Failed`, `Rejected`
                - Or use EnumClass (Recommended): `CertificateStatus`. e.g. `CertificateStatus.accepted`

        - Returns:
            - call_result.InstallCertificate
        """
        return call_result.InstallCertificate(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.InstallCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.InstallCertificate
        """
        return call_result.InstallCertificate(
            status = dict_data['status']
        )

