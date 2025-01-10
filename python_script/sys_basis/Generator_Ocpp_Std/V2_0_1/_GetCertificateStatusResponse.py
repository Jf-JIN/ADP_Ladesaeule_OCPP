from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class GenGetCertificateStatusResponse(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | GetCertificateStatusType,
        status_info: dict | None = None,
        ocsp_result: str | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetCertificateStatus:
        """
        Generate GetCertificateStatusResponse

        - Args: 
            - status(str): 
                - This indicates whether the charging station was able to retrieve the OCSP certificate status. 
                - Enum: `Accepted`, `Failed`
                - Or use EnumClass (Recommended): `GetCertificateStatusType`. e.g. `GetCertificateStatusType.accepted`
            - status_info(dict|None): 
                - Element providing more information about the status. 
                - recommended to use `get_status_info()` to set element
            - ocsp_result(str|None): 
                - OCSPResponse class as defined in <<ref-ocpp_security_24, IETF RFC 6960>>. DER encoded (as defined in <<ref-ocpp_security_24, IETF RFC 6960>>), and then base64 encoded. MAY only be omitted when status is not Accepted. 
                - length limit: [1, 5500]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call_result.GetCertificateStatus
        """
        return call_result.GetCertificateStatus(
            status=status,
            status_info=status_info,
            ocsp_result=ocsp_result,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetCertificateStatus:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.GetCertificateStatus
        """
        return call_result.GetCertificateStatus(
            status=dict_data['status'],
            status_info=dict_data.get('statusInfo', None),
            ocsp_result=dict_data.get('ocspResult', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_status_info(
        reason_code: str,
        additional_info: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get status info

        - Args: 
            - reason_code(str): 
                - A predefined code for the reason why the status is returned in this response. The string is case-insensitive. 
                - length limit: [1, 20]
            - additional_info(str|None): 
                - Additional text to provide detailed information. 
                - length limit: [1, 512]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'reasonCode': reason_code
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
