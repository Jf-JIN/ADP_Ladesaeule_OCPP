from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class sign_certificate_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        csr: str
    ) -> call.SignCertificate:
        """
        Generate SignCertificateRequest

        - Args: 
            - csr(str): 
                - length limit: [1, 5500]

        - Returns:
            - call.SignCertificate
        """
        return call.SignCertificate(
            csr = csr
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
            csr = dict_data['csr']
        )

