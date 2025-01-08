from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class send_local_list_request(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        list_version: int,
        update_type: str | UpdateType,
        local_authorization_list: list | None = None
    ) -> call.SendLocalList:
        """
        Generate SendLocalListRequest

        - Args: 
            - list_version(int): 
            - update_type(str|UpdateType): 
                - Enum: `Differential`, `Full`
                - Or use EnumClass (Recommended): `UpdateType`. e.g. `UpdateType.differential`
            - local_authorization_list(list|None): 
                - recommended to use `get_local_authorization_list()` to set element or to build a custom list.

        - Returns:
            - call.SendLocalList
        """
        return call.SendLocalList(
            list_version = list_version,
            update_type = update_type,
            local_authorization_list = local_authorization_list
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SendLocalList:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SendLocalList
        """
        return call.SendLocalList(
            list_version = dict_data['listVersion'],
            update_type = dict_data['updateType'],
            local_authorization_list = dict_data.get('localAuthorizationList', None)
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
        temp_dict:dict = {
            'status': status
        }
        if expiry_date is not None:
            temp_dict['expiryDate'] = expiry_date
        if parent_id_tag is not None:
            temp_dict['parentIdTag'] = parent_id_tag
        return temp_dict


    @staticmethod
    def get_local_authorization_list(
        id_tag: str,
        id_tag_info: dict | None = None
    ) -> dict:
        """
        Get local authorization list

        - Args: 
            - id_tag(str): 
                - length limit: [1, 20]
            - id_tag_info(dict|None): 
                - recommended to use `get_id_tag_info()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'idTag': id_tag
        }
        if id_tag_info is not None:
            temp_dict['idTagInfo'] = id_tag_info
        return temp_dict

