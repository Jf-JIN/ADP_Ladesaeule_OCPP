from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class delete_certificate_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | DeleteCertificateStatus
    ) -> call_result.DeleteCertificate:
        """
        Generate DeleteCertificateResponse

        - Args: 
            - status(str|DeleteCertificateStatus): 
                - Enum: `Accepted`, `Failed`, `NotFound`
                - Or use EnumClass (Recommended): `DeleteCertificateStatus`. e.g. `DeleteCertificateStatus.accepted`

        - Returns:
            - call_result.DeleteCertificate
        """
        return call_result.DeleteCertificate(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DeleteCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.DeleteCertificate
        """
        return call_result.DeleteCertificate(
            status = dict_data['status']
        )

