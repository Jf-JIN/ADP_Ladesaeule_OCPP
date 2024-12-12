
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class cancel_reservation(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call.CancelReservation:
        """
        生成 CancelReservation

        参数:
        - 

        返回值:
        - call.CancelReservation
        """
        return call.CancelReservation(
            
        )

