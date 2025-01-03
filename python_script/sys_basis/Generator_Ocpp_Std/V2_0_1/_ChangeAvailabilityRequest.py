
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class change_availability_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(operational_status, evse=None, custom_data=None) -> call.ChangeAvailability:
        """
        生成 ChangeAvailabilityRequest

        参数:
            -

        返回值:
            - call.ChangeAvailability
        """
        return call.ChangeAvailability(
            operational_status = operational_status,
            evse = evse,
            custom_data = custom_data
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
            operational_status = dict_data['operationalStatus'],
            evse = dict_data.get('evse', None),
            custom_data = dict_data.get('customData', None)
        )

