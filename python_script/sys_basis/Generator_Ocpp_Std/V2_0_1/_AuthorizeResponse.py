from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class authorize_response(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        id_token_info: dict,
        certificate_status: str | AuthorizeCertificateStatusType | None = None,
        custom_data: dict | None = None
    ) -> call_result.Authorize:
        """
        生成 AuthorizeResponse

        - 参数: 
            - id_token_info(dict): 
                - ID_ Token 包含有关标识符的状态信息. 建议不要停止对计费期间过期的令牌进行计费, 因为 ExpiryDate 仅用于缓存目的. 如果未给出 ExpiryDate, 则状态没有结束日期. 
                - 推荐使用 `get_id_token_info()` 传入
            - certificate_status(str||None): 
                - 证书状态信息. -如果所有证书均有效: 返回"已接受". -如果其中一份证书被撤销, 则返回'CertificateRevoked'. 
                - 枚举值: `Accepted`, `SignatureError`, `CertificateExpired`, `CertificateRevoked`, `NoCertificateAvailable`, `CertChainError`, `ContractCancelled`
                - 或使用枚举类(推荐)`AuthorizeCertificateStatusType`. e.g. `AuthorizeCertificateStatusType.accepted`
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
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

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call_result.Authorize
        """
        return call_result.Authorize(
            id_token_info=dict_data['idTokenInfo'],
            certificate_status=dict_data.get('certificateStatus', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 additional info

        - 参数: 
            - additional_id_token(str): 
                - 该字段指定附加的IdToken. 
                - 长度范围: [1, 36]
            - type(str): 
                - 这定义了additionalIdToken的类型. 这是自定义类型, 因此实现需要所有相关方都同意. 
                - 长度范围: [1, 50]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_group_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 group id token

        - 参数: 
            - id_token(str): 
                - IdToken 不区分大小写. 可能包含 RFID 标签的隐藏 ID, 但也可以包含 UUID. 
                - 长度范围: [1, 36]
            - type(str): 
                - 枚举可能的 idToken 类型. 
                - 枚举值: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - 或使用枚举类(推荐)`IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - 包含用于授权的不区分大小写的标识符以及支持多种形式的标识符的授权类型. 
                - 推荐使用 `get_additional_info()` 传入列表元素 或 自行创建列表.
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_personal_message(
        format: str | MessageFormatType,
        content: str,
        language: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 personal message

        - 参数: 
            - format(str): 
                - 消息_内容. 格式. Message_ Format_ Code 消息格式. 
                - 枚举值: `ASCII`, `HTML`, `URI`, `UTF8`
                - 或使用枚举类(推荐)`MessageFormatType`. e.g. `MessageFormatType.ascii`
            - content(str): 
                - 息_内容. 内容. 留言内容 留言内容. 
                - 长度范围: [1, 512]
            - language(str|None): 
                - 消息_内容. 语言. Language_ Code 消息语言标识符. 包含 <<ref-RFC5646,[RFC5646]>> 中定义的语言代码. 
                - 长度范围: [1, 8]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'format': format,
            'content': content
        }
        if language is not None:
            temp_dict['language'] = language
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_id_token_info(
        status: str | AuthorizationStatusType,
        cache_expiry_date_time: str | None = None,
        charging_priority: int | None = None,
        language1: str | None = None,
        evse_id: list | None = None,
        group_id_token: dict | None = None,
        language2: str | None = None,
        personal_message: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 id token info

        - 参数: 
            - status(str): 
                - ID_令牌. 地位. Authorization_ Status ID 令牌的当前状态. 
                - 枚举值: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`
                - 或使用枚举类(推荐)`AuthorizationStatusType`. e.g. `AuthorizationStatusType.accepted`
            - cache_expiry_date_time(str|None): 
                - ID_令牌. 到期. Date_ Time 令牌必须被视为无效的日期和时间. 
                - 格式: date-time
            - charging_priority(int|None): 
                - 从商业角度来看优先. 默认优先级为0, 范围为-9到9. 值越高表示优先级越高. <<transactioneventresponse,TransactionEventResponse>> 中的chargingPriority 否决了这一点. 
            - language1(str|None): 
                - ID_令牌. 语言1. Language_ Code 标识符用户的首选用户界面语言. 包含<<ref-RFC5646,[RFC5646]>>中定义的语言代码. 
                - 长度范围: [1, 8]
            - evse_id(list|None): 
                - 推荐使用 `get_evse_id()` 传入列表元素 或 自行创建列表.
            - group_id_token(dict|None): 
                - 包含用于授权的不区分大小写的标识符以及支持多种形式的标识符的授权类型. 
                - 推荐使用 `get_group_id_token()` 传入
            - language2(str|None): 
                - ID_令牌. 语言2. Language_Code 标识符用户的第二首选用户界面语言. 省略 language1 时请勿使用, 必须与 language1 不同. 包含<<ref-RFC5646,[RFC5646]>>中定义的语言代码. 
                - 长度范围: [1, 8]
            - personal_message(dict|None): 
                - Message_ Content 包含要在充电站上显示的消息的消息详细信息. 
                - 推荐使用 `get_personal_message()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'status': status
        }
        if cache_expiry_date_time is not None:
            temp_dict['cacheExpiryDateTime'] = cache_expiry_date_time
        if charging_priority is not None:
            temp_dict['chargingPriority'] = charging_priority
        if language1 is not None:
            temp_dict['language1'] = language1
        if evse_id is not None:
            temp_dict['evseId'] = evse_id
        if group_id_token is not None:
            temp_dict['groupIdToken'] = group_id_token
        if language2 is not None:
            temp_dict['language2'] = language2
        if personal_message is not None:
            temp_dict['personalMessage'] = personal_message
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
