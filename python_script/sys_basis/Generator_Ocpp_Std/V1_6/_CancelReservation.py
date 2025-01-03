
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class cancel_reservation(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate() -> call.CancelReservation:
        """
        生成 CancelReservation

        参数:
            - 

        返回值:
            - call.CancelReservation
        """
        return call.CancelReservation(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.CancelReservation:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.CancelReservation
        """
        return call.CancelReservation(
            
        )

