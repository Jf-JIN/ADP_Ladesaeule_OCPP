
class Base_OCPP_Struct_V2_0_1(object):
    def get_custom_data(self, vendor_id: str) -> dict:
        """
        生成 CustomData

        参数:
            vendor_id(str): 厂商ID (1-255 个字符)

        返回值: 
            CustomData(dict)
        """
        return {
            "vendorId": vendor_id
        }
