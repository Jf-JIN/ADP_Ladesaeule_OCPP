import jsonschema
try:
    from ._Base import *
except:
    from _Base import *


class authorize_request(Base_OCPP_Struct_V2_0_1):
    def generate(self, id_token, custom_data: None = None, certificate: str | None = None, hash_data: list | None = None):
        """ 
        生成 AuthorizeRequest

        参数：
        - id_token(str): 候选为
        - custom_data(dict|None): 推荐使用 ``get_custom_data()`` 传入
        - certificate(str|None): 
        - hash_data(list|None): 候选为 ``SHA256`` ``SHA384`` ``SHA512``

        返回值：
            AuthorizeRequest
        """

        pass

    def get_id_tocken(self, id_token: str, type: str, custom_data: dict | None = None, additional_info: dict | None = None):
        """
        生成 IdToken

        参数：
            id_token(str): 候选为
            type(str): 类型 候选：Central eMAID ISO14443 ISO15693 KeyCode Local MacAddress NoAuthorization
            custom_data(dict|None): 推荐使用 get_custom_data() 传入
            additional_info(list|None): 推荐使用 get_additional_info() 传入

        返回值：
            IdToken
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

    def get_custom_data(self, vendor_id: str) -> dict:
        """
        生成 CustomData

        参数:
            vendor_id(str): 厂商ID (1-255 个字符)

        返回值：
            CustomData(dict)
        """
        return {
            "vendorId": vendor_id
        }

    def get_certificate(self):
        pass

    def get_additional_info(self, additional_id_token: str, type: str, custom_data: dict | None = None) -> dict:
        """ 
        生成 AdditionalInfo

        参数：
            additional_id_token(str): 附加的ID令牌，长度为 1-36 个字符
            type(str): 类型 (1-36 个字符)
            custom_data(dict|None): 推荐使用 get_custom_data() 传入

        返回值：
            AdditionalInfo(dict)
        """
        temp_dict = {
            "additionalIdToken": additional_id_token,
            "type": type
        }
        if custom_data:
            temp_dict["customData"] = custom_data
        return temp_dict
