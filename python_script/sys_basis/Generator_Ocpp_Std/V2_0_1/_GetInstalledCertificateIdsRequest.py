from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_installed_certificate_ids_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        certificate_type: list | None = None,
        custom_data: dict | None = None
    ) -> call.GetInstalledCertificateIds:
        """
        Generate GetInstalledCertificateIdsRequest

        - Args: 
            - certificate_type(list|None): 
                - recommended to use `get_certificate_type()` to set element or to build a custom list.
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.GetInstalledCertificateIds
        """
        return call.GetInstalledCertificateIds(
            certificate_type = certificate_type,
            custom_data = custom_data
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
            certificate_type = dict_data.get('certificateType', None),
            custom_data = dict_data.get('customData', None)
        )

