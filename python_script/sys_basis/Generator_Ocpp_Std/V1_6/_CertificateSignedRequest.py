from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class certificate_signed_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        certificate_chain: str
    ) -> call.CertificateSigned:
        """
        Generate CertificateSignedRequest

        - Args: 
            - certificate_chain(str): 
                - length limit: [1, 10000]

        - Returns:
            - call.CertificateSigned
        """
        return call.CertificateSigned(
            certificate_chain = certificate_chain
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
            certificate_chain = dict_data['certificateChain']
        )

