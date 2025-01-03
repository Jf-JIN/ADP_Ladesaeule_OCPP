
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class send_local_list(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(list_version, update_type, local_authorization_list) -> call.SendLocalList:
        """
        生成 SendLocalList

        参数:
            -

        返回值:
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
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SendLocalList
        """
        return call.SendLocalList(
            list_version = dict_data['listVersion'],
            update_type = dict_data['updateType'],
            local_authorization_list = dict_data['localAuthorizationList']
        )

