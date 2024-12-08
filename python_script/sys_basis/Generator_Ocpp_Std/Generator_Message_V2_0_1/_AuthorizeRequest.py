import jsonschema
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *


class authorize_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(id_token, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None) -> dict:
        """ 
        生成 AuthorizeRequest

        参数: 
        - id_token(str): 推荐使用 `get_id_tocken()` 传入
        - custom_data(dict|None): 推荐使用 `get_custom_data()` 传入
        - certificate(str|None): 长度为 1-5500 个字符
        - hash_data(list|None): 推荐使用 `get_hash_data_list()` 传入

        返回值: 
        - AuthorizeRequest
        """
        temp_dict = {
            "idToken": id_token
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if certificate is not None:
            temp_dict["certificate"] = certificate
        if hash_data is not None:
            temp_dict["hashData"] = hash_data
        try:
            jsonschema.validate(temp_dict, STD_v2_0_1.AuthorizeRequest)
        except jsonschema.ValidationError as e:
            raise jsonschema.ValidationError(f"<authorize_request> 生成器 错误: {e.message}")
        return temp_dict

    @staticmethod
    def get_id_tocken(id_token: str, type: str, custom_data: dict | None = None, additional_info: dict | None = None) -> dict:
        """
        生成 IdToken

        参数: 
        - id_token(str): id令牌, 长度为 1-36 个字符
        - type(str): 类型 候选: `Central` `eMAID` `ISO14443` `ISO15693` `KeyCode` `Local` `MacAddress` `NoAuthorization`
        - custom_data(dict|None): 推荐使用 `get_custom_data()` 传入
        - additional_info(list|None): 推荐使用 `get_additional_info_list()` 传入

        返回值: 
        - IdToken(dict)
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
        - AdditionalInfo(list)
        """
        return [*additional_info]

    @staticmethod
    def get_additional_info(additional_id_token: str, type: str, custom_data: dict | None = None) -> dict:
        """ 
        生成 AdditionalInfo

        参数: 
        - additional_id_token(str): 附加的ID令牌, 长度为 1-36 个字符
        - type(str): 类型 (1-36 个字符)
        - custom_data(dict|None): 推荐使用 get_custom_data() 传入

        返回值: 
        - AdditionalInfo(dict)
        """
        temp_dict = {
            "additionalIdToken": additional_id_token,
            "type": type
        }
        if custom_data:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_hash_data_list(*hash_data: dict) -> list:
        """ 
        生成 iso15118CertificateHashData

        参数: 
        - *hash_data(dict): 推荐使用 `get_hash_data()` 传入

        返回值: 
        - iso15118CertificateHashData(list)
        """
        return [*hash_data]

    @staticmethod
    def get_hash_data(hash_algorithm: str, issuer_name_hash: str, issuer_key_hash: str, serial_number: str, responder_url: str, custom_data: dict | None = None) -> dict:
        """ 
        生成 HashData

        参数: 
        - hash_algorithm(str): 哈希算法 `SHA256` `SHA384` `SHA512`
        - issuer_name_hash(str): 发行者名称哈希 (1-128 个字符)
        - issuer_key_hash(str): 发行者密钥哈希 (1-128 个字符)
        - serial_number(str): 序列号 (1-40 个字符)
        - responder_url(str): 响应者 URL (1-512 个字符)
        - custom_data(dict|None): 推荐使用 get_custom_data() 传入

        """
        temp = {
            "hashAlgorithm": hash_algorithm,
            "issuerNameHash": issuer_name_hash,
            "issuerKeyHash": issuer_key_hash,
            "serialNumber": serial_number,
            "responderURL": responder_url
        }
        if custom_data:
            temp["customData"] = custom_data
        return temp
