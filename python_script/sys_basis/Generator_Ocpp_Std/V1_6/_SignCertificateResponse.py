from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenSignCertificateResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | GenericStatus
    ) -> call_result.SignCertificate:
        """
        Generate SignCertificateResponse

        - Args: 
            - status(str|GenericStatus): 
                - Enum: `Accepted`, `Rejected`
                - Or use EnumClass (Recommended): `GenericStatus`. e.g. `GenericStatus.accepted`

        - Returns:
            - call_result.SignCertificate
        """
        return call_result.SignCertificate(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.SignCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.SignCertificate
        """
        return call_result.SignCertificate(
            status = dict_data['status']
        )

