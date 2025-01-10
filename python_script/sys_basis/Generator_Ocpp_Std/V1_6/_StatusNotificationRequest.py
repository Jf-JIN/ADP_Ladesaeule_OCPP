from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenStatusNotificationRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        error_code: str | ChargePointErrorCode,
        status: str | ChargePointStatus,
        info: str | None = None,
        timestamp: str | None = None,
        vendor_id: str | None = None,
        vendor_error_code: str | None = None
    ) -> call.StatusNotification:
        """
        Generate StatusNotificationRequest

        - Args: 
            - connector_id(int): 
            - error_code(str|ChargePointErrorCode): 
                - Enum: `ConnectorLockFailure`, `EVCommunicationError`, `GroundFailure`, `HighTemperature`, `InternalError`, `LocalListConflict`, `NoError`, `OtherError`, `OverCurrentFailure`, `PowerMeterFailure`, `PowerSwitchFailure`, `ReaderFailure`, `ResetFailure`, `UnderVoltage`, `OverVoltage`, `WeakSignal`
                - Or use EnumClass (Recommended): `ChargePointErrorCode`. e.g. `ChargePointErrorCode.connector_lock_failure`
            - status(str|ChargePointStatus): 
                - Enum: `Available`, `Preparing`, `Charging`, `SuspendedEVSE`, `SuspendedEV`, `Finishing`, `Reserved`, `Unavailable`, `Faulted`
                - Or use EnumClass (Recommended): `ChargePointStatus`. e.g. `ChargePointStatus.available`
            - info(str|None): 
                - length limit: [1, 50]
            - timestamp(str|None): 
                - format: date-time
            - vendor_id(str|None): 
                - length limit: [1, 255]
            - vendor_error_code(str|None): 
                - length limit: [1, 50]

        - Returns:
            - call.StatusNotification
        """
        return call.StatusNotification(
            connector_id = connector_id,
            error_code = error_code,
            status = status,
            info = info,
            timestamp = timestamp,
            vendor_id = vendor_id,
            vendor_error_code = vendor_error_code
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.StatusNotification
        """
        return call.StatusNotification(
            connector_id = dict_data['connectorId'],
            error_code = dict_data['errorCode'],
            status = dict_data['status'],
            info = dict_data.get('info', None),
            timestamp = dict_data.get('timestamp', None),
            vendor_id = dict_data.get('vendorId', None),
            vendor_error_code = dict_data.get('vendorErrorCode', None)
        )

