from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenInstallCertificateRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        certificate_type: str | CertificateUse,
        certificate: str
    ) -> call.InstallCertificate:
        """
        Generate InstallCertificateRequest

        - Args: 
            - certificate_type(str|CertificateUse): 
                - Enum: `CentralSystemRootCertificate`, `ManufacturerRootCertificate`
                - Or use EnumClass (Recommended): `CertificateUse`. e.g. `CertificateUse.central_system_root_certificate`
            - certificate(str): 
                - length limit: [1, 5500]

        - Returns:
            - call.InstallCertificate
        """
        return call.InstallCertificate(
            certificate_type = certificate_type,
            certificate = certificate
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.InstallCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.InstallCertificate
        """
        return call.InstallCertificate(
            certificate_type = dict_data['certificateType'],
            certificate = dict_data['certificate']
        )

