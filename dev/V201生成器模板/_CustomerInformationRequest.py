
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class customer_information_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call.CustomerInformation:
        """
        生成 CustomerInformationRequest

        参数:
            - 

        返回值:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.CustomerInformation:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.CustomerInformation
        """
        return call.CustomerInformation(
            
        )

