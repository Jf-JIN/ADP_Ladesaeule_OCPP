
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class clear_cache_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.ClearCache:
        """
        生成 ClearCacheResponse

        参数:
        - 

        返回值:
        - call_result.ClearCache
        """
        return call_result.ClearCache(
            
        )

