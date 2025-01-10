from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenNotifyCustomerInformationRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        data: str,
        seq_no: int,
        generated_at: str,
        request_id: int,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call.NotifyCustomerInformation:
        """
        Generate NotifyCustomerInformationRequest

        - Args: 
            - data(str): 
                - (Part of) the requested data. No format specified in which the data is returned. Should be human readable. 
                - length limit: [1, 512]
            - seq_no(int): 
                - Sequence number of this message. First message starts at 0. 
            - generated_at(str): 
                -  Timestamp of the moment this message was generated at the Charging Station. 
                - format: date-time
            - request_id(int): 
                - The Id of the request. 
            - tbc(bool|None): 
                - "to be continued" indicator. Indicates whether another part of the monitoringData follows in an upcoming notifyMonitoringReportRequest message. Default value when omitted is false. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.NotifyCustomerInformation
        """
        return call.NotifyCustomerInformation(
            data=data,
            seq_no=seq_no,
            generated_at=generated_at,
            request_id=request_id,
            tbc=tbc,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyCustomerInformation:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.NotifyCustomerInformation
        """
        return call.NotifyCustomerInformation(
            data=dict_data['data'],
            seq_no=dict_data['seqNo'],
            generated_at=dict_data['generatedAt'],
            request_id=dict_data['requestId'],
            tbc=dict_data.get('tbc', None),
            custom_data=dict_data.get('customData', None)
        )
