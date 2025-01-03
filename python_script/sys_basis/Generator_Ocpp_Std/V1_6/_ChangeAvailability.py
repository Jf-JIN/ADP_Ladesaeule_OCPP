
from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class change_availability(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(connector_id, type) -> call.ChangeAvailability:
        """
        生成 ChangeAvailability

        参数:
            -

        返回值:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            connector_id = connector_id,
            type = type
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ChangeAvailability:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            connector_id = dict_data['connectorId'],
            type = dict_data['type']
        )

