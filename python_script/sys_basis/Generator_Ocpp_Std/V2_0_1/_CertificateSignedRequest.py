from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class certificate_signed_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        certificate_chain: str,
        certificate_type: str | CertificateSigningUseType | None = None,
        custom_data: dict | None = None
    ) -> call.CertificateSigned:
        """
        Generate CertificateSignedRequest

        - Args: 
            - certificate_chain(str): 
                - The signed PEM encoded X.509 certificate. This can also contain the necessary sub CA certificates. In that case, the order of the bundle should follow the certificate chain, starting from the leaf certificate. The Configuration Variable <<configkey-max-certificate-chain-size,MaxCertificateChainSize>> can be used to limit the maximum size of this field. 
                - length limit: [1, 10000]
            - certificate_type(str||None): 
                - Indicates the type of the signed certificate that is returned. When omitted the certificate is used for both the 15118 connection (if implemented) and the Charging Station to CSMS connection. This field is required when a typeOfCertificate was included in the <<signcertificaterequest,SignCertificateRequest>> that requested this certificate to be signed AND both the 15118 connection and the Charging Station connection are implemented. 
                - Enum: `ChargingStationCertificate`, `V2GCertificate`
                - Or use EnumClass (Recommended): `CertificateSigningUseType`. e.g. `CertificateSigningUseType.charging_station_certificate`
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.CertificateSigned
        """
        return call.CertificateSigned(
            certificate_chain = certificate_chain,
            certificate_type = certificate_type,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CertificateSigned:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.CertificateSigned
        """
        return call.CertificateSigned(
            certificate_chain = dict_data['certificateChain'],
            certificate_type = dict_data.get('certificateType', None),
            custom_data = dict_data.get('customData', None)
        )

