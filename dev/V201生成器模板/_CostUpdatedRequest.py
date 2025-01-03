
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class cost_updated_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(total_cost, transaction_id, custom_data=None) -> call.CostUpdated:
        """
        生成 CostUpdatedRequest

        参数:
            -

        返回值:
            - call.CostUpdated
        """
        return call.CostUpdated(
            total_cost = total_cost,
            transaction_id = transaction_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CostUpdated:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.CostUpdated
        """
        return call.CostUpdated(
            total_cost = dict_data['totalCost'],
            transaction_id = dict_data['transactionId'],
            custom_data = dict_data.get('customData', None)
        )

