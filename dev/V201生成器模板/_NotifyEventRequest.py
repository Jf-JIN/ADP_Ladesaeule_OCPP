
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_event_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(generated_at, seq_no, event_data, tbc=None, custom_data=None) -> call.NotifyEvent:
        """
        生成 NotifyEventRequest

        参数:
            -

        返回值:
            - call.NotifyEvent
        """
        return call.NotifyEvent(
            generated_at = generated_at,
            seq_no = seq_no,
            event_data = event_data,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEvent:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.NotifyEvent
        """
        return call.NotifyEvent(
            generated_at = dict_data['generatedAt'],
            seq_no = dict_data['seqNo'],
            event_data = dict_data['eventData'],
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

