
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class get_local_list_version_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data=None) -> call.GetLocalListVersion:
        """
        生成 GetLocalListVersionRequest

        参数:
            -

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetLocalListVersion:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            custom_data = dict_data.get('customData', None)
        )

