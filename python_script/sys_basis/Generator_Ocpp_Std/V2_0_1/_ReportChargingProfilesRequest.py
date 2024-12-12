
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class report_charging_profiles_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(**kwargs) -> call.ReportChargingProfiles:
        """
        生成 ReportChargingProfilesRequest

        参数:
        - 

        返回值:
        - call.ReportChargingProfiles
        """
        return call.ReportChargingProfiles(
            
        )

