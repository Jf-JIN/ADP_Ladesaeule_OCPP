from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenCostUpdatedRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        total_cost: int | float,
        transaction_id: str,
        custom_data: dict | None = None
    ) -> call.CostUpdated:
        """
        Generate CostUpdatedRequest

        - Args: 
            - total_cost(int|float): 
                - Current total cost, based on the information known by the CSMS, of the transaction including taxes. In the currency configured with the configuration Variable: [<<configkey-currency, Currency>>] 
            - transaction_id(str): 
                - Transaction Id of the transaction the current cost are asked for. 
                - length limit: [1, 36]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.CostUpdated
        """
        return call.CostUpdated(
            total_cost=total_cost,
            transaction_id=transaction_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.CostUpdated:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.CostUpdated
        """
        return call.CostUpdated(
            total_cost=dict_data['totalCost'],
            transaction_id=dict_data['transactionId'],
            custom_data=dict_data.get('customData', None)
        )
