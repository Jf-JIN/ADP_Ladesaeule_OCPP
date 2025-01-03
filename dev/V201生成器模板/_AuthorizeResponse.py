
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class authorize_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id_token_info, certificate_status=None, custom_data=None) -> call_result.Authorize:
        """
        生成 AuthorizeResponse

        参数:
            -

        返回值:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_token_info = id_token_info,
            certificate_status = certificate_status,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Authorize:
        """
        加载字典数据，将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_token_info = dict_data['idTokenInfo'],
            certificate_status = dict_data.get('certificateStatus', None),
            custom_data = dict_data.get('customData', None)
        )

