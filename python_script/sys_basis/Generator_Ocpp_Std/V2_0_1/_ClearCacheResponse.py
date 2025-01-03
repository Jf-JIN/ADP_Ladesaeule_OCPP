
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class clear_cache_response(Base_OCPP_Struct_V2_0_1): 

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

