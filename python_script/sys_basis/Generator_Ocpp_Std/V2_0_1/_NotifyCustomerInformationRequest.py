
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_customer_information_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.NotifyCustomerInformation:
        """
        生成 NotifyCustomerInformationRequest

        参数:
        - 

        返回值:
        - call.NotifyCustomerInformation
        """
        return call.NotifyCustomerInformation(
            
        )

