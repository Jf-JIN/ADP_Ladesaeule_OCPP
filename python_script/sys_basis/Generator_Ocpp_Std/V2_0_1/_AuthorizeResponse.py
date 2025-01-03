
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class authorize_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id_token_info: dict, certificate_status: str | AuthorizeCertificateStatusType | None = None, custom_data: dict | None = None) -> call_result.Authorize:
        """ 
        生成AuthorizeResponse

        参数: 
            - id_token_info(dict): 推荐使用 `id_token_info.generate()` 生成
            - certificate_status(str|AuthorizeCertificateStatusType): 证书状态
                - `Accepted`, `SignatureError`, `CertificateExpired`, `CertificateRevoked`, `NoCertificateAvailable`, `CertChainError`, `ContractCancelled` .
                - 或者使用 `AuthorizeCertificateStatusType` 枚举, 例如 `AuthorizeCertificateStatusType.Accepted` .
            - custom_data(dict): 推荐使用 `get_custom_data()` 生成

        返回值:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_token_info=id_token_info,
            certificate_status=certificate_status,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Authorize:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_token_info=dict_data['idTokenInfo'],
            certificate_status=dict_data.get('certificateStatus', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_id_token_info(status: str | AuthorizationStatusType, custom_data: dict | None = None, cache_expiry_date_time: str | None = None, charging_priority: int | None = None, evse_id: list | None = None, group_id_token: dict | None = None, language1: str | None = None, language2: str | None = None, personal_message: dict | None = None) -> dict:
        """ 
        获取id_token_info

        参数: 
            - status(str): 状态 
                - `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown` .
                - 或者使用 `AuthorizationStatusType` 枚举, 如 `AuthorizationStatusType.Accepted` .
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 生成
            - cache_expiry_date_time(str): 过期时间, 格式如:2024-12-09
            - charging_priority(int): 充电优先级, 范围: [-9, 9], 默认值: 0
            - evse_id(list): 充电桩id, 推荐使用 `get_evse_id()` 生成
            - group_id_token(dict): 组id令牌, 推荐使用 `get_group_id_token()` 生成
            - language1(str): 首选界面语言, 标准为`RFC 5646`, 格式如: en-US, 最大长度为 8 个字符
            - language2(str): 备选界面语言, 标准为`RFC 5646`, 格式如: en-US, 最大长度为 8 个字符
            - personal_message(dict): 个人消息, 推荐使用 `get_personal_message()` 生成

        返回值:
            - id_token_info(dict)
        """
        temp_dict = {
            'status': status
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        if cache_expiry_date_time is not None:
            temp_dict['cacheExpiryDateTime'] = cache_expiry_date_time
        if charging_priority is not None:
            temp_dict['chargingPriority'] = charging_priority
        if evse_id is not None:
            temp_dict['evseId'] = evse_id
        if group_id_token is not None:
            temp_dict['groupIdToken'] = group_id_token
        if language1 is not None:
            temp_dict['language1'] = language1
        if language2 is not None:
            temp_dict['language2'] = language2
        if personal_message is not None:
            temp_dict['personalMessage'] = personal_message
        return temp_dict

    @staticmethod
    def get_evse_id(*evse_id: int) -> list:
        """ 
        生成 evse_id

        参数:
            - evse_id(int), 可接受多个参数

        返回值:
            - evse_id(list)
        """
        return [*evse_id]

    @staticmethod
    def get_group_id_tocken(id_token: str, type: str | IdTokenType, custom_data: dict | None = None, additional_info: dict | None = None) -> dict:
        """
        生成 groupIdToken

        参数:
            - id_token(str): id令牌, 长度为 [1-36] 个字符
            - type(str|IdTokenType): 类型 
                - `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization` .
                - 或者使用 `IdTokenType` 枚举类, 例如 `IdTokenType.Central` .
            - custom_data(dict|None): 推荐使用 `get_custom_data()` 传入
            - additional_info(list|None): 推荐使用 `get_additional_info_list()` 传入

        返回值:
            - group_id_tocken(dict)
        """
        temp_dict = {
            "idToken": id_token,
            "type": type
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if additional_info is not None:
            temp_dict["additionalInfo"] = additional_info
        return temp_dict

    @staticmethod
    def get_additional_info_list(*additional_info: dict) -> list:
        """
        生成 AdditionalInfo列表

        参数:
            - *additional_info(dict): 推荐使用 `get_additional_info()` 传入

        返回值:
            - additional_info(list)
        """
        return [*additional_info]

    @staticmethod
    def get_additional_info(additional_id_token: str, type: str, custom_data: dict | None = None) -> dict:
        """
        生成 AdditionalInfo

        参数:
            - additional_id_token(str): 附加的ID令牌, 长度为 [1-36] 个字符
            - type(str): 类型, 长度为 [1-36] 个字符
            - custom_data(dict|None): 推荐使用 get_custom_data() 传入

        返回值:
            - additional_info(dict)
        """
        temp_dict = {
            "additionalIdToken": additional_id_token,
            "type": type
        }
        if custom_data:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_personal_message(format: str | MessageFormatType, content: str, language: str | None = None, custom_data: str | None = None) -> dict:
        """ 
        生成 PersonalMessage

        参数:
            - format(str): 格式 
                - `ASCII`, `HTML`, `URI`, `UTF8` .
                - 或者使用 `MessageFormatType` 枚举, 如: `MessageFormatType.ASCII` .
            - content(str): 内容, 长度为 [1-512] 个字符
            - language(str): 语言, 标准为`RFC 5646`, 格式如: en-US, 长度为 [0-8] 个字符
            - custom_data(dict): 推荐使用 `get_custom_data()` 生成

        返回值:
            - personal_message(dict)
        """
        temp_dict = {
            'format': format,
            'content': content
        }
        if language is not None:
            temp_dict['language'] = language
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
