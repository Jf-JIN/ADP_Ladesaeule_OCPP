
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class send_local_list(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.SendLocalList:
        """
        生成 SendLocalList

        参数:
        - 

        返回值:
        - call.SendLocalList
        """
        return call.SendLocalList(
            
        )

