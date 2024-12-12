import os

dirpath = os.path.dirname(__file__)

v16 = ['Authorize', 'AuthorizeResponse', 'BootNotification', 'BootNotificationResponse', 'CancelReservation', 'CancelReservationResponse', 'ChangeAvailability', 'ChangeAvailabilityResponse', 'ChangeConfiguration', 'ChangeConfigurationResponse', 'ClearCache', 'ClearCacheResponse', 'ClearChargingProfile', 'ClearChargingProfileResponse', 'DataTransfer', 'DataTransferResponse', 'DiagnosticsStatusNotification', 'DiagnosticsStatusNotificationResponse', 'FirmwareStatusNotification', 'FirmwareStatusNotificationResponse', 'GetCompositeSchedule', 'GetCompositeScheduleResponse', 'GetConfiguration', 'GetConfigurationResponse', 'GetDiagnostics', 'GetDiagnosticsResponse',
       'GetLocalListVersion', 'GetLocalListVersionResponse', 'Heartbeat', 'HeartbeatResponse', 'MeterValues', 'MeterValuesResponse', 'RemoteStartTransaction', 'RemoteStartTransactionResponse', 'RemoteStopTransaction', 'RemoteStopTransactionResponse', 'ReserveNow', 'ReserveNowResponse', 'Reset', 'ResetResponse', 'SendLocalList', 'SendLocalListResponse', 'SetChargingProfile', 'SetChargingProfileResponse', 'StartTransaction', 'StartTransactionResponse', 'StatusNotification', 'StatusNotificationResponse', 'StopTransaction', 'StopTransactionResponse', 'TriggerMessage', 'TriggerMessageResponse', 'UnlockConnector', 'UnlockConnectorResponse', 'UpdateFirmware', 'UpdateFirmwareResponse']

v201 = ['UpdateFirmwareResponse', 'UpdateFirmwareRequest', 'UnpublishFirmwareResponse', 'UnpublishFirmwareRequest', 'UnlockConnectorResponse', 'UnlockConnectorRequest', 'TriggerMessageResponse', 'TriggerMessageRequest', 'TransactionEventResponse', 'TransactionEventRequest', 'StatusNotificationResponse', 'StatusNotificationRequest', 'SignCertificateResponse', 'SignCertificateRequest', 'SetVariablesResponse', 'SetVariablesRequest', 'SetVariableMonitoringResponse', 'SetVariableMonitoringRequest', 'SetNetworkProfileResponse', 'SetNetworkProfileRequest', 'SetMonitoringLevelResponse', 'SetMonitoringLevelRequest', 'SetMonitoringBaseResponse', 'SetMonitoringBaseRequest', 'SetDisplayMessageResponse', 'SetDisplayMessageRequest', 'SetChargingProfileResponse', 'SetChargingProfileRequest', 'SendLocalListResponse', 'SendLocalListRequest', 'SecurityEventNotificationResponse', 'SecurityEventNotificationRequest', 'ResetResponse', 'ResetRequest', 'ReserveNowResponse', 'ReserveNowRequest', 'ReservationStatusUpdateResponse', 'ReservationStatusUpdateRequest', 'RequestStopTransactionResponse', 'RequestStopTransactionRequest', 'RequestStartTransactionResponse', 'RequestStartTransactionRequest', 'ReportChargingProfilesResponse', 'ReportChargingProfilesRequest', 'PublishFirmwareStatusNotificationResponse', 'PublishFirmwareStatusNotificationRequest', 'PublishFirmwareResponse', 'PublishFirmwareRequest', 'NotifyReportResponse', 'NotifyReportRequest', 'NotifyMonitoringReportResponse', 'NotifyMonitoringReportRequest', 'NotifyEventResponse', 'NotifyEventRequest', 'NotifyEVChargingScheduleResponse', 'NotifyEVChargingScheduleRequest', 'NotifyEVChargingNeedsResponse', 'NotifyEVChargingNeedsRequest', 'NotifyDisplayMessagesResponse', 'NotifyDisplayMessagesRequest', 'NotifyCustomerInformationResponse', 'NotifyCustomerInformationRequest', 'NotifyChargingLimitResponse',
        'NotifyChargingLimitRequest', 'MeterValuesResponse', 'MeterValuesRequest', 'LogStatusNotificationResponse', 'LogStatusNotificationRequest', 'InstallCertificateResponse', 'InstallCertificateRequest', 'HeartbeatResponse', 'HeartbeatRequest', 'GetVariablesResponse', 'GetVariablesRequest', 'GetTransactionStatusResponse', 'GetTransactionStatusRequest', 'GetReportResponse', 'GetReportRequest', 'GetMonitoringReportResponse', 'GetMonitoringReportRequest', 'GetLogResponse', 'GetLogRequest', 'GetLocalListVersionResponse', 'GetLocalListVersionRequest', 'GetInstalledCertificateIdsResponse', 'GetInstalledCertificateIdsRequest', 'GetDisplayMessagesResponse', 'GetDisplayMessagesRequest', 'GetCompositeScheduleResponse', 'GetCompositeScheduleRequest', 'GetChargingProfilesResponse', 'GetChargingProfilesRequest', 'GetCertificateStatusResponse', 'GetCertificateStatusRequest', 'GetBaseReportResponse', 'GetBaseReportRequest', 'Get15118EVCertificateResponse', 'Get15118EVCertificateRequest', 'FirmwareStatusNotificationResponse', 'FirmwareStatusNotificationRequest', 'DeleteCertificateResponse', 'DeleteCertificateRequest', 'DataTransferResponse', 'DataTransferRequest', 'CustomerInformationResponse', 'CustomerInformationRequest', 'CostUpdatedResponse', 'CostUpdatedRequest', 'ClearVariableMonitoringResponse', 'ClearVariableMonitoringRequest', 'ClearedChargingLimitResponse', 'ClearedChargingLimitRequest', 'ClearDisplayMessageResponse', 'ClearDisplayMessageRequest', 'ClearChargingProfileResponse', 'ClearChargingProfileRequest', 'ClearCacheResponse', 'ClearCacheRequest', 'ChangeAvailabilityResponse', 'ChangeAvailabilityRequest', 'CertificateSignedResponse', 'CertificateSignedRequest', 'CancelReservationResponse', 'CancelReservationRequest', 'BootNotificationResponse', 'BootNotificationRequest', 'AuthorizeResponse', 'AuthorizeRequest']


def camel_to_snake(name):
    result = []
    for char in name:
        char: str
        if char.isupper():
            if result:
                result.append('_')
            result.append(char.lower())
        else:
            result.append(char)
    result_str = ''.join(result)
    return result_str.replace('_e_v_', '_ev_')


def create_file(version):
    if version == '201' or version == 201:
        list_f = v201
        import_str = 'V2_0_1'
        ocpp_version = 'ocpp.v201'
    elif version == 16 or version == '16':
        list_f = v16
        import_str = 'V1_6'
        ocpp_version = 'ocpp.v16'
    else:
        print(f'重新输入版本, 可供候选: 201 16')
    for i in list_f:
        file_path = os.path.join(dirpath, f'_{i}.py')
        std_dataclass_name = os.path.basename(file_path).replace('Response.py', '').replace('Request.py', '').strip('_').replace('.py', '')
        if 'Response' in i:
            call_struct_import = 'call_result'
            data_class_name = 'call_result.' + std_dataclass_name
        else:
            call_struct_import = 'call'
            data_class_name = 'call.' + std_dataclass_name
        text = f'''
from {ocpp_version}.enums import *
from {ocpp_version} import {call_struct_import}
from ._Base import *


class {camel_to_snake(i)}(Base_OCPP_Struct_{import_str}): 

    @staticmethod
    def generate(**kwargs) -> {data_class_name}:
        """
        生成 {i}

        参数:
        - 

        返回值:
        - {data_class_name}
        """
        return {data_class_name}(
            
        )

'''
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)


create_file(201)
