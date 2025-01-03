
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_monitoring_base_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate() -> call.SetMonitoringBase:
        """
        生成 SetMonitoringBaseRequest

        参数:
            - 

        返回值:
            - call.SetMonitoringBase
        """
        return call.SetMonitoringBase(
            
        )
    
    @staticmethod
    def load_dict(dict_data: dict) -> call.SetMonitoringBase:
        """ 
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetMonitoringBase
        """
        return call.SetMonitoringBase(
            
        )

