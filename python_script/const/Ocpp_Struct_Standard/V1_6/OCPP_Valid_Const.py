
from .OCPP_All_Standard import (_Authorize, _AuthorizeResponse, _BootNotification, _BootNotificationResponse, _CancelReservation, _CancelReservationResponse, _ChangeAvailability, _ChangeAvailabilityResponse, _ChangeConfiguration, _ChangeConfigurationResponse, _ClearCache, _ClearCacheResponse, _ClearChargingProfile, _ClearChargingProfileResponse, _DataTransfer, _DataTransferResponse, _DiagnosticsStatusNotification, _DiagnosticsStatusNotificationResponse, _FirmwareStatusNotification, _FirmwareStatusNotificationResponse, _GetCompositeSchedule, _GetCompositeScheduleResponse, _GetConfiguration, _GetConfigurationResponse, _GetDiagnostics, _GetDiagnosticsResponse, _GetLocalListVersion, _GetLocalListVersionResponse, _Heartbeat, _HeartbeatResponse, _MeterValues, _MeterValuesResponse, _RemoteStartTransaction, _RemoteStartTransactionResponse, _RemoteStopTransaction, _RemoteStopTransactionResponse, _ReserveNow, _ReserveNowResponse, _Reset, _ResetResponse, _SendLocalList, _SendLocalListResponse, _SetChargingProfile, _SetChargingProfileResponse, _StartTransaction, _StartTransactionResponse, _StatusNotification, _StatusNotificationResponse, _StopTransaction, _StopTransactionResponse, _TriggerMessage, _TriggerMessageResponse, _UnlockConnector, _UnlockConnectorResponse, _UpdateFirmware, _UpdateFirmwareResponse)
from const.Analog_Define import AnalogDefine


class STD_v1_6(AnalogDefine):

    Authorize = _Authorize
    AuthorizeResponse = _AuthorizeResponse
    BootNotification = _BootNotification
    BootNotificationResponse = _BootNotificationResponse
    CancelReservation = _CancelReservation
    CancelReservationResponse = _CancelReservationResponse
    ChangeAvailability = _ChangeAvailability
    ChangeAvailabilityResponse = _ChangeAvailabilityResponse
    ChangeConfiguration = _ChangeConfiguration
    ChangeConfigurationResponse = _ChangeConfigurationResponse
    ClearCache = _ClearCache
    ClearCacheResponse = _ClearCacheResponse
    ClearChargingProfile = _ClearChargingProfile
    ClearChargingProfileResponse = _ClearChargingProfileResponse
    DataTransfer = _DataTransfer
    DataTransferResponse = _DataTransferResponse
    DiagnosticsStatusNotification = _DiagnosticsStatusNotification
    DiagnosticsStatusNotificationResponse = _DiagnosticsStatusNotificationResponse
    FirmwareStatusNotification = _FirmwareStatusNotification
    FirmwareStatusNotificationResponse = _FirmwareStatusNotificationResponse
    GetCompositeSchedule = _GetCompositeSchedule
    GetCompositeScheduleResponse = _GetCompositeScheduleResponse
    GetConfiguration = _GetConfiguration
    GetConfigurationResponse = _GetConfigurationResponse
    GetDiagnostics = _GetDiagnostics
    GetDiagnosticsResponse = _GetDiagnosticsResponse
    GetLocalListVersion, = _GetLocalListVersion,
    GetLocalListVersionResponse = _GetLocalListVersionResponse
    Heartbeat = _Heartbeat
    HeartbeatResponse = _HeartbeatResponse
    MeterValues = _MeterValues
    MeterValuesResponse = _MeterValuesResponse
    RemoteStartTransaction = _RemoteStartTransaction
    RemoteStartTransactionResponse = _RemoteStartTransactionResponse
    RemoteStopTransaction = _RemoteStopTransaction
    RemoteStopTransactionResponse = _RemoteStopTransactionResponse
    ReserveNow = _ReserveNow
    ReserveNowResponse = _ReserveNowResponse
    Reset = _Reset
    ResetResponse = _ResetResponse
    SendLocalList = _SendLocalList
    SendLocalListResponse = _SendLocalListResponse
    SetChargingProfile = _SetChargingProfile
    SetChargingProfileResponse = _SetChargingProfileResponse
    StartTransaction = _StartTransaction
    StartTransactionResponse = _StartTransactionResponse
    StatusNotification = _StatusNotification
    StatusNotificationResponse = _StatusNotificationResponse
    StopTransaction = _StopTransaction
    StopTransactionResponse = _StopTransactionResponse
    TriggerMessage = _TriggerMessage
    TriggerMessageResponse = _TriggerMessageResponse
    UnlockConnector = _UnlockConnector
    UnlockConnectorResponse = _UnlockConnectorResponse
    UpdateFirmware = _UpdateFirmware
    UpdateFirmwareResponse = _UpdateFirmwareResponse
