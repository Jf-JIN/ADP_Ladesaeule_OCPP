from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenGetInstalledCertificateIdsRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        certificate_type: str | CertificateUse
    ) -> call.GetInstalledCertificateIds:
        """
        Generate GetInstalledCertificateIdsRequest

        - Args: 
            - certificate_type(str|CertificateUse): 
                - Enum: `CentralSystemRootCertificate`, `ManufacturerRootCertificate`
                - Or use EnumClass (Recommended): `CertificateUse`. e.g. `CertificateUse.central_system_root_certificate`

        - Returns:
            - call.GetInstalledCertificateIds
        """
        return call.GetInstalledCertificateIds(
            certificate_type = certificate_type
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetInstalledCertificateIds:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.GetInstalledCertificateIds
        """
        return call.GetInstalledCertificateIds(
            certificate_type = dict_data['certificateType']
        )

