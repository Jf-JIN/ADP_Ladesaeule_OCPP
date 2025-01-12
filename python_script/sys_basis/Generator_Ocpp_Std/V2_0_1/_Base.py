
class Base_OCPP_Struct_V2_0_1(object):
    @staticmethod
    def get_custom_data(vendor_id: str, **kwargs) -> dict:
        """
        生成 CustomData

        - 参数:
            - vendor_id(str): 厂商ID (1-255 个字符)
            - **kwargs: 额外的关键字参数内容

        - 返回值: 
            - CustomData(dict)
        """
        custom_data = {
            "vendorId": vendor_id
        }
        custom_data.update(kwargs)  # 将额外的关键字参数加入字典
        return custom_data
