
from ocpp.v201.enums import *
from ocpp.v201 import call_result
from ._Base import *


class report_charging_profiles_response(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call_result.ReportChargingProfiles:
        """
        生成 ReportChargingProfilesResponse

        参数:
            - 

        返回值:
            - call_result.ReportChargingProfiles
        """
        return call_result.ReportChargingProfiles(
            
        )

