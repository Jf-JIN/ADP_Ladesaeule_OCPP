
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class transaction_event_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(total_cost=None, charging_priority=None, id_token_info=None, updated_personal_message=None, custom_data=None) -> call_result.TransactionEvent:
        """
        生成 TransactionEventResponse

        参数:
            -

        返回值:
            - call_result.TransactionEvent
        """
        return call_result.TransactionEvent(
            total_cost = total_cost,
            charging_priority = charging_priority,
            id_token_info = id_token_info,
            updated_personal_message = updated_personal_message,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.TransactionEvent:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.TransactionEvent
        """
        return call_result.TransactionEvent(
            total_cost = dict_data.get('totalCost', None),
            charging_priority = dict_data.get('chargingPriority', None),
            id_token_info = dict_data.get('idTokenInfo', None),
            updated_personal_message = dict_data.get('updatedPersonalMessage', None),
            custom_data = dict_data.get('customData', None)
        )

