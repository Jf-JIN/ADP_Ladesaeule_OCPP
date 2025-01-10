from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenHeartbeatRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        
    ) -> call.Heartbeat:
        """
        Generate HeartbeatRequest

        - Args: 
            

        - Returns:
            - call.Heartbeat
        """
        return call.Heartbeat(
            
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.Heartbeat:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.Heartbeat
        """
        return call.Heartbeat(
            
        )

