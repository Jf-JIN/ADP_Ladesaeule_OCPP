
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class transaction_event_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(id_token_info: dict | None,
                 updated_personal_message: dict | None,
                 total_cost: int | float | None = None,
                 charging_priority: int | None = None,
                 custom_data: dict | None = None,
                 **kwargs) -> call_result.TransactionEvent:
        """
        生成 TransactionEventResponse

        参数:
            - total_cost(int|float): 只有充电结束后才会发送总的花费，含税.
            - charging_priority(int): 充电优先级,范围从-9到+9，默认为0.
            - id_token_info(dict): 推荐使用 `get_id_token_info()` 传入
            - updated_personal_message(dict): 推荐使用 `get_personal_message()` 传入
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - call_result.TransactionEvent
        """
        return call_result.TransactionEvent(
            total_cost=total_cost or kwargs.get("total_cost", None),
            charging_priority=charging_priority or kwargs.get("charging_priority", None),
            id_token_info=id_token_info or kwargs.get("id_token_info", None),
            updated_personal_message=updated_personal_message or kwargs.get("updated_personal_message", None),
            custom_data=custom_data or kwargs.get("custom_data", None),
        )

    @staticmethod
    def get_personal_message(message_format: str | MessageFormatType, content: str, language: str | None = None, custom_data: dict | None = None) -> dict:
        """
        生成 PersonalMessage

        参数:
            - message_format(str): 信息目录的格式, `ASCII`,`HTML`,`URI`,`UTF8`
            - content（str）: 信息的目录，字符串长度为[1-512]
            - language(str): 信息目录的语言, 字符串长度为[1-8]
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - personal_message(dict)
        """

        temp_dict = {
            "messageFormat": message_format,
            "content": content
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if language is not None:
            temp_dict["language"] = language
        return temp_dict

    @staticmethod
    def get_id_token_info(status: str | AuthorizationStatusType, cache_expiry_date_time: str | None = None, 
                          charging_priority: int | None = None, language_1: str | None = None,
                          evse_id: int | None = None, group_id_token: dict | None = None, language_2: str | None = None,
                          personal_message: dict | None = None, custom_data: dict | None = None) -> dict:

        """
        生成 IdTokenInfo

        参数:
            -status(str|AuthorizationStatusType):ID_ Token的状态（授权状态）
                - 字符串, 无先后顺序和分组, 仅是逻辑分组:
                - `Accepted`,`Blocked`,`ConcurrentTx`,`Expired`,`Invalid`,`NoCredit`,`NotAllowedTypeEVSE`,
                - `NotAtThisLocation`,`NotAtThisTime`,`Unknown`
            -cache_expiry_date_time(str): 有效日期,字符串格式为"date-time"
            -charging_priority(int): 充电优先级，范围是-9到+9，默认是0.
            -language_1(str): 语言1，字符串长度为[1-8]
            -evse_id(int):仅在 IdToken 仅对一个或多个特定的 EVSE有效，而非整个充电站时使用.????关于evse_id的我可能有写错，指的是正文而不是注释！
            -group_id_token(dict):推荐使用 `get_id_tocken()` 传入
            -language_2(str):语言2，字符串长度为[1-8]
            -personal_message(ditc):推荐使用 `get_personal_message()` 传入
            -custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - id_token_info(dict)
        """

        temp_dict = {
            "status": status
        }
        if cache_expiry_date_time is not None:
            temp_dict["cacheWxpiryDateTime"] = cache_expiry_date_time
        if charging_priority is not None:
            temp_dict["chargingPriority"] = charging_priority
        if language_1 is not None:
            temp_dict["language1"] = language_1
        if evse_id is not None:
            temp_dict["evseId"] = evse_id
        if group_id_token is not None:
            temp_dict["groupIdToken"] = group_id_token
        if language_2 is not None:
            temp_dict["language2"] = language_2
        if personal_message is not None:
            temp_dict["personalMessage"] = personal_message
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_id_tocken(id_token: str, id_token_type: str | IdTokenType, custom_data: dict | None = None,
                      additional_info: dict | None = None) -> dict:
        """
        生成 IdToken

        参数:
            - id_token(str): id令牌, 长度为 [1-36] 个字符
            - id_token_type(str|IdTokenType): 类型 候选:
                - `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization` .
                - 或者可以使用 `IdTokenType` 枚举, 例如: `IdTokenType.central` .
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入
            - additional_info(list): 推荐使用 `get_additional_info_list()` 传入

        返回值:
            - id_tocken(dict)
        """
        temp_dict = {
            "idToken": id_token,
            "idTokenType": id_token_type
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if additional_info is not None:
            temp_dict["additionalInfo"] = additional_info
        return temp_dict
