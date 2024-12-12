
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class clear_cache(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.ClearCache:
        """
        生成 ClearCache

        参数:
        - 

        返回值:
        - call.ClearCache
        """
        return call.ClearCache(
            
        )

