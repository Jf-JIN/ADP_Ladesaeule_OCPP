from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class publish_firmware_status_notification_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        status: str | PublishFirmwareStatusType,
        location: list | None = None,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call.PublishFirmwareStatusNotification:
        """
        Generate PublishFirmwareStatusNotificationRequest

        - Args: 
            - status(str): 
                - This contains the progress status of the publishfirmware installation. 
                - Enum: `Idle`, `DownloadScheduled`, `Downloading`, `Downloaded`, `Published`, `DownloadFailed`, `DownloadPaused`, `InvalidChecksum`, `ChecksumVerified`, `PublishFailed`
                - Or use EnumClass (Recommended): `PublishFirmwareStatusType`. e.g. `PublishFirmwareStatusType.idle`
            - location(list|None): 
                - recommended to use `get_location()` to set element or to build a custom list.
            - request_id(int|None): 
                - The request id that was provided in the PublishFirmwareRequest which triggered this action. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.PublishFirmwareStatusNotification
        """
        return call.PublishFirmwareStatusNotification(
            status = status,
            location = location,
            request_id = request_id,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.PublishFirmwareStatusNotification:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.PublishFirmwareStatusNotification
        """
        return call.PublishFirmwareStatusNotification(
            status = dict_data['status'],
            location = dict_data.get('location', None),
            request_id = dict_data.get('requestId', None),
            custom_data = dict_data.get('customData', None)
        )

