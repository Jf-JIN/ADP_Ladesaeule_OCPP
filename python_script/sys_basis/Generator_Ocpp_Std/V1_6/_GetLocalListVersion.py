
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class get_local_list_version(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate() -> call.GetLocalListVersion:
        """
        生成 GetLocalListVersion

        参数:
            -

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.GetLocalListVersion:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.GetLocalListVersion
        """
        return call.GetLocalListVersion(
            
        )

