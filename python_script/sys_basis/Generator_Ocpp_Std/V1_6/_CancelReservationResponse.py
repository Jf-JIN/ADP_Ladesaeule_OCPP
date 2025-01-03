
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class cancel_reservation_response(Base_OCPP_Struct_V1_6): 

    @staticmethod
    def generate(**kwargs) -> call_result.CancelReservation:
        """
        生成 CancelReservationResponse

        参数:
            - 

        返回值:
            - call_result.CancelReservation
        """
        return call_result.CancelReservation(
            
        )

