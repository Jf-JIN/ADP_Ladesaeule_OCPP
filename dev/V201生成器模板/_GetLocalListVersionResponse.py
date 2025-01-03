
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class get_local_list_version_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(version_number, custom_data=None) -> call_result.GetLocalListVersion:
        """
        生成 GetLocalListVersionResponse

        参数:
            -

        返回值:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            version_number = version_number,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.GetLocalListVersion:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.GetLocalListVersion
        """
        return call_result.GetLocalListVersion(
            version_number = dict_data['versionNumber'],
            custom_data = dict_data.get('customData', None)
        )

