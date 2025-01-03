
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class cancel_reservation_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.CancelReservation:
        """
        生成 CancelReservationRequest

        参数:
            - 

        返回值:
            - call.CancelReservation
        """
        return call.CancelReservation(
            
        )

