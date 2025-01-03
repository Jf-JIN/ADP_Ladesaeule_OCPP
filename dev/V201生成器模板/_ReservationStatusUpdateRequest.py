
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class reservation_status_update_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(reservation_id, reservation_update_status, custom_data=None) -> call.ReservationStatusUpdate:
        """
        生成 ReservationStatusUpdateRequest

        参数:
            -

        返回值:
            - call.ReservationStatusUpdate
        """
        return call.ReservationStatusUpdate(
            reservation_id = reservation_id,
            reservation_update_status = reservation_update_status,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReservationStatusUpdate:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ReservationStatusUpdate
        """
        return call.ReservationStatusUpdate(
            reservation_id = dict_data['reservationId'],
            reservation_update_status = dict_data['reservationUpdateStatus'],
            custom_data = dict_data.get('customData', None)
        )

