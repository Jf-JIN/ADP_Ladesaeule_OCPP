
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class authorize(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(id_tag) -> call.Authorize:
        """
        生成 Authorize

        参数:
            -

        返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_tag = id_tag
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Authorize:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_tag = dict_data['idTag']
        )

