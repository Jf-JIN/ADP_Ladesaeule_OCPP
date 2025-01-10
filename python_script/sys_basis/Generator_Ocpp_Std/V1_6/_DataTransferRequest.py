from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenDataTransferRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        vendor_id: str,
        message_id: str | None = None,
        data: str | None = None
    ) -> call.DataTransfer:
        """
        Generate DataTransferRequest

        - Args: 
            - vendor_id(str): 
                - length limit: [1, 255]
            - message_id(str|None): 
                - length limit: [1, 50]
            - data(str|None): 

        - Returns:
            - call.DataTransfer
        """
        return call.DataTransfer(
            vendor_id = vendor_id,
            message_id = message_id,
            data = data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.DataTransfer:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.DataTransfer
        """
        return call.DataTransfer(
            vendor_id = dict_data['vendorId'],
            message_id = dict_data.get('messageId', None),
            data = dict_data.get('data', None)
        )

