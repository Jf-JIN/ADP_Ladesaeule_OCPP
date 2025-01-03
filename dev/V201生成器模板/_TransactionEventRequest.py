
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class transaction_event_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(event_type, timestamp, trigger_reason, seq_no, transaction_info, meter_value=None, offline=None, number_of_phases_used=None, cable_max_current=None, reservation_id=None, evse=None, id_token=None, custom_data=None) -> call.TransactionEvent:
        """
        生成 TransactionEventRequest

        参数:
            -

        返回值:
            - call.TransactionEvent
        """
        return call.TransactionEvent(
            event_type = event_type,
            timestamp = timestamp,
            trigger_reason = trigger_reason,
            seq_no = seq_no,
            transaction_info = transaction_info,
            meter_value = meter_value,
            offline = offline,
            number_of_phases_used = number_of_phases_used,
            cable_max_current = cable_max_current,
            reservation_id = reservation_id,
            evse = evse,
            id_token = id_token,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.TransactionEvent:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.TransactionEvent
        """
        return call.TransactionEvent(
            event_type = dict_data['eventType'],
            timestamp = dict_data['timestamp'],
            trigger_reason = dict_data['triggerReason'],
            seq_no = dict_data['seqNo'],
            transaction_info = dict_data['transactionInfo'],
            meter_value = dict_data.get('meterValue', None),
            offline = dict_data.get('offline', None),
            number_of_phases_used = dict_data.get('numberOfPhasesUsed', None),
            cable_max_current = dict_data.get('cableMaxCurrent', None),
            reservation_id = dict_data.get('reservationId', None),
            evse = dict_data.get('evse', None),
            id_token = dict_data.get('idToken', None),
            custom_data = dict_data.get('customData', None)
        )

