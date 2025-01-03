
from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class cancel_reservation_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(status) -> call_result.CancelReservation:
        """
        生成 CancelReservationResponse

        参数:
            -

        返回值:
            - call_result.CancelReservation
        """
        return call_result.CancelReservation(
            status = status
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.CancelReservation:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.CancelReservation
        """
        return call_result.CancelReservation(
            status = dict_data['status']
        )

