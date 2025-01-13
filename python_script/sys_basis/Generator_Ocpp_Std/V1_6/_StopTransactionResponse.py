from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenStopTransactionResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        id_tag_info: dict | None = None
    ) -> call_result.StopTransaction:
        """
        Generate StopTransactionResponse

        - Args: 
            - id_tag_info(dict|None): 
                - recommended to use `get_id_tag_info()` to set element

        - Returns:
            - call_result.StopTransaction
        """
        return call_result.StopTransaction(
            id_tag_info=id_tag_info
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.StopTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.StopTransaction
        """
        return call_result.StopTransaction(
            id_tag_info=dict_data.get('idTagInfo', None)
        )

    @staticmethod
    def get_id_tag_info(
        status: str | AuthorizationStatus,
        expiry_date: str | None = None,
        parent_id_tag: str | None = None
    ) -> dict:
        """
        Get id tag info

        - Args: 
            - status(str|AuthorizationStatus): 
                - Enum: `Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx`
                - Or use EnumClass (Recommended): `AuthorizationStatus`. e.g. `AuthorizationStatus.accepted`
            - expiry_date(str|None): 
                - format: date-time
            - parent_id_tag(str|None): 
                - length limit: [1, 20]

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'status': status
        }
        if expiry_date is not None:
            temp_dict['expiryDate'] = expiry_date
        if parent_id_tag is not None:
            temp_dict['parentIdTag'] = parent_id_tag
        return temp_dict
