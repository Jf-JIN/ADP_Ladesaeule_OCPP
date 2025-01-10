from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenSignCertificateRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        csr: str,
        certificate_type: str | CertificateSigningUseType | None = None,
        custom_data: dict | None = None
    ) -> call.SignCertificate:
        """
        Generate SignCertificateRequest

        - Args: 
            - csr(str): 
                - The Charging Station SHALL send the public key in form of a Certificate Signing Request (CSR) as described in RFC 2986 [22] and then PEM encoded, using the <<signcertificaterequest,SignCertificateRequest>> message. 
                - length limit: [1, 5500]
            - certificate_type(str||None): 
                - Indicates the type of certificate that is to be signed. When omitted the certificate is to be used for both the 15118 connection (if implemented) and the Charging Station to CSMS connection. 
                - Enum: `ChargingStationCertificate`, `V2GCertificate`
                - Or use EnumClass (Recommended): `CertificateSigningUseType`. e.g. `CertificateSigningUseType.charging_station_certificate`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SignCertificate
        """
        return call.SignCertificate(
            csr=csr,
            certificate_type=certificate_type,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SignCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SignCertificate
        """
        return call.SignCertificate(
            csr=dict_data['csr'],
            certificate_type=dict_data.get('certificateType', None),
            custom_data=dict_data.get('customData', None)
        )
