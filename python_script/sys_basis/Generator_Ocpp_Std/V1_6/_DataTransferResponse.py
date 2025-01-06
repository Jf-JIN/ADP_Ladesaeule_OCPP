from ocpp.v16.enums import *
from ocpp.v16 import call_result
from ._Base import *


class data_transfer_response(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        status: str | DataTransferStatus,
        data: str | None = None
    ) -> call_result.DataTransfer:
        """
        Generate DataTransferResponse

        - Args: 
            - status(str|DataTransferStatus): 
                - Enum: `Accepted`, `Rejected`, `UnknownMessageId`, `UnknownVendorId`
                - Or use EnumClass (Recommended): `DataTransferStatus`. e.g. `DataTransferStatus.accepted`
            - data(str|None): 

        - Returns:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status = status,
            data = data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call_result.DataTransfer:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call_result.DataTransfer
        """
        return call_result.DataTransfer(
            status = dict_data['status'],
            data = dict_data.get('data', None)
        )

