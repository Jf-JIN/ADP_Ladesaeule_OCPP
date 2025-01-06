from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class install_certificate_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        certificate_type: str | InstallCertificateUseType,
        certificate: str,
        custom_data: dict | None = None
    ) -> call.InstallCertificate:
        """
        Generate InstallCertificateRequest

        - Args: 
            - certificate_type(str): 
                - Indicates the certificate type that is sent. 
                - Enum: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `ManufacturerRootCertificate`
                - Or use EnumClass (Recommended): `InstallCertificateUseType`. e.g. `InstallCertificateUseType._v2g_root_certificate`
            - certificate(str): 
                - A PEM encoded X.509 certificate. 
                - length limit: [1, 5500]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.InstallCertificate
        """
        return call.InstallCertificate(
            certificate_type = certificate_type,
            certificate = certificate,
            custom_data = custom_data
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
            certificate = dict_data['certificate'],
            custom_data = dict_data.get('customData', None)
        )

