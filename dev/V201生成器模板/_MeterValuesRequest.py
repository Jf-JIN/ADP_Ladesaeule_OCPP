
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class meter_values_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(evse_id, meter_value, custom_data=None) -> call.MeterValues:
        """
        生成 MeterValuesRequest

        参数:
            -

        返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            evse_id = evse_id,
            meter_value = meter_value,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.MeterValues:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            evse_id = dict_data['evseId'],
            meter_value = dict_data['meterValue'],
            custom_data = dict_data.get('customData', None)
        )

