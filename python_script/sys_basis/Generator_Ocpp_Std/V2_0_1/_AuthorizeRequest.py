from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenAuthorizeRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        id_token: dict,
        certificate: str | None = None,
        iso15118_certificate_hash_data: list | None = None,
        custom_data: dict | None = None
    ) -> call.Authorize:
        """
        生成 AuthorizeRequest

        - 参数: 
            - id_token(dict): 
                - 包含用于授权的不区分大小写的标识符以及支持多种形式的标识符的授权类型. 
                - 推荐使用 `get_id_tocken()` 传入
            - certificate(str|None): 
                - 由 EV 提供并以 PEM 格式编码的 X.509 证书. 
                - 长度范围: [1, 5500]
            - iso15118_certificate_hash_data(list|None): 
                - 长度范围: [1, 4]
                - 推荐使用 `get_hash_data_list()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_token=id_token,
            certificate=certificate,
            iso15118_certificate_hash_data=iso15118_certificate_hash_data,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Authorize:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.Authorize
        """
        return call.Authorize(
            id_token=dict_data['idToken'],
            certificate=dict_data.get('certificate', None),
            iso15118certificate_hash_data=dict_data.get('iso15118CertificateHashData', None),
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
                - 定义了additionalIdToken的类型. 这是自定义类型, 因此实现需要所有相关方都同意. 
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
    def get_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 id token

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
    def get_iso15118certificate_hash_data(
        hash_algorithm: str | HashAlgorithmType,
        issuer_name_hash: str,
        issuer_key_hash: str,
        serial_number: str,
        responder_url: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 iso15118certificate hash data

        - 参数: 
            - hash_algorithm(str): 
                - 所提供的哈希所使用的算法. 
                - 枚举值: `SHA256`, `SHA384`, `SHA512`
                - 或使用枚举类(推荐)`HashAlgorithmType`. e.g. `HashAlgorithmType.sha256`
            - issuer_name_hash(str): 
                - 发行者 DN(专有名称)的哈希值. 
                - 长度范围: [1, 128]
            - issuer_key_hash(str): 
                - 发行者公钥的哈希值
                - 长度范围: [1, 128]
            - serial_number(str): 
                - 证书的序列号. 
                - 长度范围: [1, 40]
            - responder_url(str): 
                - 这包含响应者 URL(不区分大小写). 
                - 长度范围: [1, 512]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'hashAlgorithm': hash_algorithm,
            'issuerNameHash': issuer_name_hash,
            'issuerKeyHash': issuer_key_hash,
            'serialNumber': serial_number,
            'responderURL': responder_url
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
