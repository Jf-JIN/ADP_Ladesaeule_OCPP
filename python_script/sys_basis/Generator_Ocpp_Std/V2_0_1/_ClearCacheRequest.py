
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class clear_cache_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(custom_data=None) -> call.ClearCache:
        """
        生成 ClearCacheRequest

        参数:
            -

        返回值:
            - call.ClearCache
        """
        return call.ClearCache(
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ClearCache:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ClearCache
        """
        return call.ClearCache(
            custom_data = dict_data.get('customData', None)
        )

