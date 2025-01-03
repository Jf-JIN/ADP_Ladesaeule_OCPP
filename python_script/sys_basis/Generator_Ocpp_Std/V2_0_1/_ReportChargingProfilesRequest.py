
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class report_charging_profiles_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(request_id, charging_limit_source, charging_profile, evse_id, tbc=None, custom_data=None) -> call.ReportChargingProfiles:
        """
        生成 ReportChargingProfilesRequest

        参数:
            -

        返回值:
            - call.ReportChargingProfiles
        """
        return call.ReportChargingProfiles(
            request_id = request_id,
            charging_limit_source = charging_limit_source,
            charging_profile = charging_profile,
            evse_id = evse_id,
            tbc = tbc,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.ReportChargingProfiles:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.ReportChargingProfiles
        """
        return call.ReportChargingProfiles(
            request_id = dict_data['requestId'],
            charging_limit_source = dict_data['chargingLimitSource'],
            charging_profile = dict_data['chargingProfile'],
            evse_id = dict_data['evseId'],
            tbc = dict_data.get('tbc', None),
            custom_data = dict_data.get('customData', None)
        )

