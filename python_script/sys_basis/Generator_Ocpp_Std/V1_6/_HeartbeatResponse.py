from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class GenHeartbeatResponse(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        current_time: str
    ) -> call_result.Heartbeat:
        """
        Generate HeartbeatResponse

        - Args: 
            - current_time(str): 
                - format: date-time

        - Returns:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time = current_time
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.Heartbeat:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.Heartbeat
        """
        return call_result.Heartbeat(
            current_time = dict_data['currentTime']
        )

