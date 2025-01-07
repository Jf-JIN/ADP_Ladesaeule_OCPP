from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get15118_ev_certificate_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        iso15118_schema_version: str,
        action: str | CertificateActionType,
        exi_request: str,
        custom_data: dict | None = None
    ) -> call.Get15118EVCertificate:
        """
        Generate Get15118EVCertificateRequest

        - Args: 
            - iso15118_schema_version(str): 
                - Schema version currently used for the 15118 session between EV and Charging Station. Needed for parsing of the EXI stream by the CSMS. 
                - length limit: [1, 50]
            - action(str): 
                - Defines whether certificate needs to be installed or updated. 
                - Enum: `Install`, `Update`
                - Or use EnumClass (Recommended): `CertificateActionType`. e.g. `CertificateActionType.install`
            - exi_request(str): 
                - Raw CertificateInstallationReq request from EV, Base64 encoded. 
                - length limit: [1, 5600]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.Get15118EVCertificate
        """
        return call.Get15118EVCertificate(
            iso15118_schema_version=iso15118_schema_version,
            action=action,
            exi_request=exi_request,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Get15118EVCertificate:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.Get15118EVCertificate
        """
        return call.Get15118EVCertificate(
            iso15118schema_version=dict_data['iso15118SchemaVersion'],
            action=dict_data['action'],
            exi_request=dict_data['exiRequest'],
            custom_data=dict_data.get('customData', None)
        )
