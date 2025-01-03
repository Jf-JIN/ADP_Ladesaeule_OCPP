
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class reservation_status_update_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.ReservationStatusUpdate:
        """
        生成 ReservationStatusUpdateRequest

        参数:
            - 

        返回值:
            - call.ReservationStatusUpdate
        """
        return call.ReservationStatusUpdate(
            
        )

