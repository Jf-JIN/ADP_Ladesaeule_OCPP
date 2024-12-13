import os

dirpath = os.path.dirname(__file__)

v16 = ['Authorize', 'AuthorizeResponse', 'BootNotification', 'BootNotificationResponse', 'CancelReservation', 'CancelReservationResponse', 'ChangeAvailability', 'ChangeAvailabilityResponse', 'ChangeConfiguration', 'ChangeConfigurationResponse', 'ClearCache', 'ClearCacheResponse', 'ClearChargingProfile', 'ClearChargingProfileResponse', 'DataTransfer', 'DataTransferResponse', 'DiagnosticsStatusNotification', 'DiagnosticsStatusNotificationResponse', 'FirmwareStatusNotification', 'FirmwareStatusNotificationResponse', 'GetCompositeSchedule', 'GetCompositeScheduleResponse', 'GetConfiguration', 'GetConfigurationResponse', 'GetDiagnostics', 'GetDiagnosticsResponse',
       'GetLocalListVersion', 'GetLocalListVersionResponse', 'Heartbeat', 'HeartbeatResponse', 'MeterValues', 'MeterValuesResponse', 'RemoteStartTransaction', 'RemoteStartTransactionResponse', 'RemoteStopTransaction', 'RemoteStopTransactionResponse', 'ReserveNow', 'ReserveNowResponse', 'Reset', 'ResetResponse', 'SendLocalList', 'SendLocalListResponse', 'SetChargingProfile', 'SetChargingProfileResponse', 'StartTransaction', 'StartTransactionResponse', 'StatusNotification', 'StatusNotificationResponse', 'StopTransaction', 'StopTransactionResponse', 'TriggerMessage', 'TriggerMessageResponse', 'UnlockConnector', 'UnlockConnectorResponse', 'UpdateFirmware', 'UpdateFirmwareResponse']

v201 = ['AuthorizeRequest', 'AuthorizeResponse', 'BootNotificationRequest', 'BootNotificationResponse', 'CancelReservationRequest', 'CancelReservationResponse', 'CertificateSignedRequest', 'CertificateSignedResponse', 'ChangeAvailabilityRequest', 'ChangeAvailabilityResponse', 'ClearCacheRequest', 'ClearCacheResponse', 'ClearChargingProfileRequest', 'ClearChargingProfileResponse', 'ClearDisplayMessageRequest', 'ClearDisplayMessageResponse', 'ClearedChargingLimitRequest', 'ClearedChargingLimitResponse', 'ClearVariableMonitoringRequest', 'ClearVariableMonitoringResponse', 'CostUpdatedRequest', 'CostUpdatedResponse', 'CustomerInformationRequest', 'CustomerInformationResponse', 'DataTransferRequest', 'DataTransferResponse', 'DeleteCertificateRequest', 'DeleteCertificateResponse', 'FirmwareStatusNotificationRequest', 'FirmwareStatusNotificationResponse', 'Get15118EVCertificateRequest', 'Get15118EVCertificateResponse', 'GetBaseReportRequest', 'GetBaseReportResponse', 'GetCertificateStatusRequest', 'GetCertificateStatusResponse', 'GetChargingProfilesRequest', 'GetChargingProfilesResponse', 'GetCompositeScheduleRequest', 'GetCompositeScheduleResponse', 'GetDisplayMessagesRequest', 'GetDisplayMessagesResponse', 'GetInstalledCertificateIdsRequest', 'GetInstalledCertificateIdsResponse', 'GetLocalListVersionRequest', 'GetLocalListVersionResponse', 'GetLogRequest', 'GetLogResponse', 'GetMonitoringReportRequest', 'GetMonitoringReportResponse', 'GetReportRequest', 'GetReportResponse', 'GetTransactionStatusRequest', 'GetTransactionStatusResponse', 'GetVariablesRequest', 'GetVariablesResponse', 'HeartbeatRequest', 'HeartbeatResponse', 'InstallCertificateRequest', 'InstallCertificateResponse', 'LogStatusNotificationRequest', 'LogStatusNotificationResponse', 'MeterValuesRequest', 'MeterValuesResponse', 'NotifyChargingLimitRequest',
        'NotifyChargingLimitResponse', 'NotifyCustomerInformationRequest', 'NotifyCustomerInformationResponse', 'NotifyDisplayMessagesRequest', 'NotifyDisplayMessagesResponse', 'NotifyEVChargingNeedsRequest', 'NotifyEVChargingNeedsResponse', 'NotifyEVChargingScheduleRequest', 'NotifyEVChargingScheduleResponse', 'NotifyEventRequest', 'NotifyEventResponse', 'NotifyMonitoringReportRequest', 'NotifyMonitoringReportResponse', 'NotifyReportRequest', 'NotifyReportResponse', 'PublishFirmwareRequest', 'PublishFirmwareResponse', 'PublishFirmwareStatusNotificationRequest', 'PublishFirmwareStatusNotificationResponse', 'ReportChargingProfilesRequest', 'ReportChargingProfilesResponse', 'RequestStartTransactionRequest', 'RequestStartTransactionResponse', 'RequestStopTransactionRequest', 'RequestStopTransactionResponse', 'ReservationStatusUpdateRequest', 'ReservationStatusUpdateResponse', 'ReserveNowRequest', 'ReserveNowResponse', 'ResetRequest', 'ResetResponse', 'SecurityEventNotificationRequest', 'SecurityEventNotificationResponse', 'SendLocalListRequest', 'SendLocalListResponse', 'SetChargingProfileRequest', 'SetChargingProfileResponse', 'SetDisplayMessageRequest', 'SetDisplayMessageResponse', 'SetMonitoringBaseRequest', 'SetMonitoringBaseResponse', 'SetMonitoringLevelRequest', 'SetMonitoringLevelResponse', 'SetNetworkProfileRequest', 'SetNetworkProfileResponse', 'SetVariableMonitoringRequest', 'SetVariableMonitoringResponse', 'SetVariablesRequest', 'SetVariablesResponse', 'SignCertificateRequest', 'SignCertificateResponse', 'StatusNotificationRequest', 'StatusNotificationResponse', 'TransactionEventRequest', 'TransactionEventResponse', 'TriggerMessageRequest', 'TriggerMessageResponse', 'UnlockConnectorRequest', 'UnlockConnectorResponse', 'UnpublishFirmwareRequest', 'UnpublishFirmwareResponse', 'UpdateFirmwareRequest', 'UpdateFirmwareResponse']


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
    elif version == '16' or version == 16:
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


def print_class_name(version):
    if version == '201' or version == 201:
        name_list = v201
    elif version == '16' or version == 16:
        name_list = v16
    else:
        print(f'重新输入版本, 可供候选: 201 16')
    temp_list = []
    for i in name_list:
        temp_list.append(camel_to_snake(i))
    print(temp_list)


def create_print_import_init(version):
    if version == '201' or version == 201:
        name_list = v201
    elif version == '16' or version == 16:
        name_list = v16
    else:
        print(f'重新输入版本, 可供候选: 201 16')
    temp_str = ''
    for i in name_list:
        temp_str += f'from ._{i} import *\n'
        # temp_str += f'from ._{i} import {camel_to_snake(i)}\n'
    print(temp_str)
    file_path = os.path.join(dirpath, '__init__.py')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(temp_str)


# print_class_name(201)


# create_print_import_init(201)


# create_file(201)
