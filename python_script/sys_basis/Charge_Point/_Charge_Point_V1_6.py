
import asyncio
import time
import traceback
from datetime import datetime
from ocpp.routing import on
from ocpp.v16.call_result import *
from const.Charge_Point_Parameters import CP_Params
from sys_basis.Generator_Ocpp_Std.V1_6 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v16 import ChargePoint as cpv16


class ChargePointV16(cpv16, ChargePointBase):
    """ 
    OCPP v1.6 信息端口类
    用于监听 ocpp 消息, 以及发送 ocpp 消息

    - 信号: 
        - signal_charge_point_ocpp_request(dict): OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        - signal_charge_point_ocpp_response(dict): OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `response_status`(int): 响应状态, 表示响应是否成功收到. 
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        - signal_charge_point_ocpp_response_result(dict): OCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `status`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`
        - signal_charge_point_info(str): 普通信号, 用于信息显示, 调试等

    - 属性: 
        - response_timeout_in_baseclass(int|float)

    - 方法: 
        - (异步)send_request_message: 发送请求消息
        - send_response_message: 发送响应消息
        - show_current_message_to_send : 显示当前待发送的消息队列
        - show_time_table_for_send_message : 显示当前待发送消息的时间表
        - set_response_timeout: 设置响应超时时间

    """

    def __init__(self, id, connection, response_timeout: int | float = 30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()
        self._set_network_buffer_time_in_baseclass(CP_Params.NETWORK_BUFFER_TIME)
        self._set_doSendDefaultResponse(CP_Params.DO_SEND_DEFAULT_RESPONSE)

    async def send_request_message(self, message):
        """ 
        发送请求消息 (不清楚调用的call会不会因版本不同而有差别, 所以写在子类这里)

        数据将通过信号 `signal_charge_point_ocpp_response` 发送回来, 数据格式如下: 
            - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
            - `ori_data`: 原始数据, 发送的Request数据
            - `data`(dict): 解包后的数据
            - `send_time`(float): 请求发送时间
            - `result`(int): 响应结果, 
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`

        当请求发送后, 将等待响应数据. 有如下三种情况: 
        1. 成功接收响应数据
        2. 超时未接收到响应数据
        3. 其他错误

        参数: 
            - message(dataclass): 请求消息对象, OCPP数据类, 如: `call.Authorize`

        返回: 
            - 无
        """
        request_time = time.time()
        try:
            response = await self.call(message)
            # signal_charge_point_ocpp_response 将在此函数发送
            self._unpack_data_and_send_signal_ocpp_response(response, request_time, ori_data=message)
        except asyncio.TimeoutError:
            self._send_signal_info(f'< Error - Request - Response_Timeout - {message.__class__.__name__} > No response was received within {self.response_timeout_in_baseclass} seconds.')
            self.signal_charge_point_ocpp_response.emit(
                {
                    'action': message.__class__.__name__,
                    'ori_data': message,
                    'data': {},
                    'send_time': request_time,
                    'result': CP_Params.RESPONSE.TIMEOUT,
                }
            )
        except Exception:
            self._send_signal_info(f'<Error - Request> {traceback.format_exc()}')
            self.signal_charge_point_ocpp_response.emit(
                {
                    'action': message.__class__.__name__,
                    'ori_data': message,
                    'data': {},
                    'send_time': request_time,
                    'result': CP_Params.RESPONSE.ERROR,
                }
            )

    @on(Action.authorize)
    async def _on_authorize_request(
        self,
        id_tag: str
    ) -> call_result.Authorize:
        default_message: Authorize = GenAuthorizeResponse.generate(
            id_tag=GenAuthorizeResponse.get_id_tag_info(
                status='Invalid')
        )
        return await self._wait_for_result(Action.authorize, default_message=default_message)

    @on(Action.boot_notification)
    async def _on_boot_notification_request(
        self,
        charge_point_vendor: str,
        charge_point_model: str,
        charge_point_serial_number: str | None = None,
        charge_box_serial_number: str | None = None,
        firmware_version: str | None = None,
        iccid: str | None = None,
        imsi: str | None = None,
        meter_type: str | None = None,
        meter_serial_number: str | None = None
    ) -> call_result.Authorize:
        default_message: BootNotification = GenBootNotificationResponse.generate(
            status=RegistrationStatus.rejected,
            current_time=datetime.now(),
            interval=60
        )
        return await self._wait_for_result(Action.boot_notification, default_message=default_message)

    @on(Action.cancel_reservation)
    async def _on_cancel_reservation_request(
        self,
        reservation_id: int
    ) -> call_result.Authorize:
        default_message: CancelReservation = GenCancelReservationResponse.generate(
            status=CancelReservationStatus.rejected
        )
        return await self._wait_for_result(Action.cancel_reservation, default_message=default_message)

    @on(Action.certificate_signed)
    async def _on_certificate_signed_request(
        self,
        certificate_chain: str
    ) -> call_result.Authorize:
        default_message: CertificateSigned = GenCertificateSignedResponse.generate(
            status=CertificateSignedStatus.rejected
        )
        return await self._wait_for_result(Action.certificate_signed, default_message=default_message)

    @on(Action.change_availability)
    async def _on_change_availability_request(
        self,
        connector_id: int,
        type: str | AvailabilityType
    ) -> call_result.Authorize:
        default_message: ChangeAvailability = GenChangeAvailabilityResponse.generate(
            status=AvailabilityStatus.rejected
        )
        return await self._wait_for_result(Action.change_availability, default_message=default_message)

    @on(Action.change_configuration)
    async def _on_change_configuration_request(
        self,
        key: str,
        value: str
    ) -> call_result.Authorize:
        default_message: ChangeConfiguration = GenChangeConfigurationResponse.generate(
            status=ConfigurationStatus.rejected
        )
        return await self._wait_for_result(Action.change_configuration, default_message=default_message)

    @on(Action.clear_cache)
    async def _on_clear_cache_request(
        self
    ) -> call_result.Authorize:
        default_message: ClearCache = GenClearCacheResponse.generate(
            status=ClearCacheStatus.rejected
        )
        return await self._wait_for_result(Action.clear_cache, default_message=default_message)

    @on(Action.clear_charging_profile)
    async def _on_clear_charging_profile_request(
        self,
        id: int | None = None,
        connector_id: int | None = None,
        charging_profile_purpose: str | ChargingProfilePurposeType | None = None,
        stack_level: int | None = None
    ) -> call_result.Authorize:
        default_message: ClearChargingProfile = GenClearChargingProfileResponse.generate(
            status=ChargingProfileStatus.rejected
        )
        return await self._wait_for_result(Action.clear_charging_profile, default_message=default_message)

    @on(Action.data_transfer)
    async def _on_data_transfer_request(
        self,
        vendor_id: str,
        message_id: str | None = None,
        data: str | None = None
    ) -> call_result.Authorize:
        default_message: DataTransfer = GenDataTransferResponse.generate(
            status=DataTransferStatus.rejected
        )
        return await self._wait_for_result(Action.data_transfer, default_message=default_message)

    @on(Action.delete_certificate)
    async def _on_delete_certificate_request(
        self,
        certificate_hash_data: dict
    ) -> call_result.Authorize:
        default_message: DeleteCertificate = GenDeleteCertificateResponse.generate(
            status=DeleteCertificateStatus.failed
        )
        return await self._wait_for_result(Action.delete_certificate, default_message=default_message)

    @on(Action.diagnostics_status_notification)
    async def _on_diagnostics_status_notification_request(
        self,
        status: str | DiagnosticsStatus
    ) -> call_result.Authorize:
        default_message: DiagnosticsStatusNotification = GenDiagnosticsStatusNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.diagnostics_status_notification, default_message=default_message)

    @on(Action.extended_trigger_message)
    async def _on_extended_trigger_message_request(
        self,
        requested_message: str | MessageTrigger,
        connector_id: int | None = None
    ) -> call_result.Authorize:
        default_message: ExtendedTriggerMessage = GenExtendedTriggerMessageResponse.generate(
            status=TriggerMessageStatus.rejected
        )
        return await self._wait_for_result(Action.extended_trigger_message, default_message=default_message)

    @on(Action.firmware_status_notification)
    async def _on_firmware_status_notification_request(
        self,
        status: str | FirmwareStatus
    ) -> call_result.Authorize:
        default_message: FirmwareStatusNotification = GenFirmwareStatusNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.firmware_status_notification, default_message=default_message)

    @on(Action.get_composite_schedule)
    async def _on_get_composite_schedule_request(
        self,
        connector_id: int,
        duration: int,
        charging_rate_unit: str | ChargingRateUnitType | None = None
    ) -> call_result.Authorize:
        default_message: GetCompositeSchedule = GenGetCompositeScheduleResponse.generate(
            status=TriggerMessageStatus.rejected
        )
        return await self._wait_for_result(Action.get_composite_schedule, default_message=default_message)

    @on(Action.get_configuration)
    async def _on_get_configuration_request(
        self,
        key: list | None = None
    ) -> call_result.Authorize:
        default_message: GetConfiguration = GenGetConfigurationResponse.generate(
        )
        return await self._wait_for_result(Action.get_configuration, default_message=default_message)

    @on(Action.get_diagnostics)
    async def _on_get_diagnostics_request(
        self,
        location: str,
        retries: int | None = None,
        retry_interval: int | None = None,
        start_time: str | None = None,
        stop_time: str | None = None
    ) -> call_result.Authorize:
        default_message: GetDiagnostics = GenGetDiagnosticsResponse.generate(
        )
        return await self._wait_for_result(Action.get_diagnostics, default_message=default_message)

    @on(Action.get_installed_certificate_ids)
    async def _on_get_installed_certificate_ids_request(
        self,
        certificate_type: str | CertificateUse
    ) -> call_result.Authorize:
        default_message: GetInstalledCertificateIds = GenGetInstalledCertificateIdsResponse.generate(
            status=GetInstalledCertificateStatus.not_found
        )
        return await self._wait_for_result(Action.get_installed_certificate_ids, default_message=default_message)

    @on(Action.get_local_list_version)
    async def _on_get_local_list_version_request(
        self
    ) -> call_result.Authorize:
        default_message: GetLocalListVersion = GenGetLocalListVersionResponse.generate(
            list_version=16
        )
        return await self._wait_for_result(Action.get_local_list_version, default_message=default_message)

    @on(Action.get_log)
    async def _on_get_log_request(
        self,
        log: dict,
        log_type: str | Log,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call_result.Authorize:
        default_message: GetLog = GenGetLogResponse.generate(
            status=LogStatus.rejected
        )
        return await self._wait_for_result(Action.get_log, default_message=default_message)

    @on(Action.heartbeat)
    async def _on_heartbeat_request(
        self
    ) -> call_result.Authorize:
        default_message: Heartbeat = GenHeartbeatResponse.generate(
            current_time=datetime.now()
        )
        return await self._wait_for_result(Action.heartbeat, default_message=default_message)

    @on(Action.install_certificate)
    async def _on_install_certificate_request(
        self,
        certificate_type: str | CertificateUse,
        certificate: str
    ) -> call_result.Authorize:
        default_message: InstallCertificate = GenInstallCertificateResponse.generate(
            status=CertificateStatus.rejected
        )
        return await self._wait_for_result(Action.install_certificate, default_message=default_message)

    @on(Action.log_status_notification)
    async def _on_log_status_notification_request(
        self,
        status: str | UploadLogStatus,
        request_id: int | None = None
    ) -> call_result.Authorize:
        default_message: LogStatusNotification = GenLogStatusNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.log_status_notification, default_message=default_message)

    @on(Action.meter_values)
    async def _on_meter_values_request(
        self,
        connector_id: int,
        meter_value: list,
        transaction_id: int | None = None
    ) -> call_result.Authorize:
        default_message: MeterValues = GenMeterValuesResponse.generate(
        )
        return await self._wait_for_result(Action.meter_values, default_message=default_message)

    @on(Action.remote_start_transaction)
    async def _on_remote_start_transaction_request(
        self,
        id_tag: str,
        connector_id: int | None = None,
        charging_profile: dict | None = None
    ) -> call_result.Authorize:
        default_message: RemoteStartTransaction = GenRemoteStartTransactionResponse.generate(
            status=RemoteStartStopStatus.rejected
        )
        return await self._wait_for_result(Action.remote_start_transaction, default_message=default_message)

    @on(Action.remote_stop_transaction)
    async def _on_remote_stop_transaction_request(
        self,
        transaction_id: int
    ) -> call_result.Authorize:
        default_message: RemoteStopTransaction = GenRemoteStopTransactionResponse.generate(
            status=RemoteStartStopStatus.rejected
        )
        return await self._wait_for_result(Action.remote_stop_transaction, default_message=default_message)

    @on(Action.reserve_now)
    async def _on_reserve_now_request(
        self,
        connector_id: int,
        expiry_date: str,
        id_tag: str,
        reservation_id: int,
        parent_id_tag: str | None = None
    ) -> call_result.Authorize:
        default_message: ReserveNow = GenReserveNowResponse.generate(
            status=ReservationStatus.rejected
        )
        return await self._wait_for_result(Action.reserve_now, default_message=default_message)

    @on(Action.reset)
    async def _on_reset_request(
        self,
        type: str | ResetType
    ) -> call_result.Authorize:
        default_message: Reset = GenResetResponse.generate(
            status=ResetStatus.rejected
        )
        return await self._wait_for_result(Action.reset, default_message=default_message)

    @on(Action.security_event_notification)
    async def _on_security_event_notification_request(
        self,
        type: str,
        timestamp: str,
        tech_info: str | None = None
    ) -> call_result.Authorize:
        default_message: SecurityEventNotification = GenSecurityEventNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.security_event_notification, default_message=default_message)

    @on(Action.send_local_list)
    async def _on_send_local_list_request(
        self,
        list_version: int,
        update_type: str | UpdateType,
        local_authorization_list: list | None = None
    ) -> call_result.Authorize:
        default_message: SendLocalList = GenSendLocalListResponse.generate(
            status=UpdateStatus.failed
        )
        return await self._wait_for_result(Action.send_local_list, default_message=default_message)

    @on(Action.set_charging_profile)
    async def _on_set_charging_profile_request(
        self,
        connector_id: int,
        cs_charging_profiles: dict
    ) -> call_result.Authorize:
        default_message: SetChargingProfile = GenSetChargingProfileResponse.generate(
            status=ChargingProfileStatus.rejected
        )
        return await self._wait_for_result(Action.set_charging_profile, default_message=default_message)

    @on(Action.sign_certificate)
    async def _on_sign_certificate_request(
        self,
        csr: str
    ) -> call_result.Authorize:
        default_message: SignCertificate = GenSignCertificateResponse.generate(
            status=GenericStatus.rejected
        )
        return await self._wait_for_result(Action.sign_certificate, default_message=default_message)

    @on(Action.signed_firmware_status_notification)
    async def _on_signed_firmware_status_notification_request(
        self,
        status: str | FirmwareStatus,
        request_id: int | None = None
    ) -> call_result.Authorize:
        default_message: SignedFirmwareStatusNotification = GenSignedFirmwareStatusNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.signed_firmware_status_notification, default_message=default_message)

    @on(Action.signed_update_firmware)
    async def _on_signed_update_firmware_request(
        self,
        request_id: int,
        firmware: dict,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call_result.Authorize:
        default_message: SignedUpdateFirmware = GenSignedUpdateFirmwareResponse.generate(
            status=UpdateFirmwareStatus.rejected
        )
        return await self._wait_for_result(Action.signed_update_firmware, default_message=default_message)

    @on(Action.start_transaction)
    async def _on_start_transaction_request(
        self,
        connector_id: int,
        id_tag: str,
        meter_start: int,
        timestamp: str,
        reservation_id: int | None = None
    ) -> call_result.Authorize:
        default_message: StartTransaction = GenStartTransactionResponse.generate(
            id_tag_info=GenStartTransactionResponse.get_id_tag_info(
                status=AuthorizationStatus.invalid
            )
        )
        return await self._wait_for_result(Action.start_transaction, default_message=default_message)

    @on(Action.status_notification)
    async def _on_status_notification_request(
        self,
        connector_id: int,
        error_code: str | ChargePointErrorCode,
        status: str | ChargePointStatus,
        info: str | None = None,
        timestamp: str | None = None,
        vendor_id: str | None = None,
        vendor_error_code: str | None = None
    ) -> call_result.Authorize:
        default_message: StatusNotification = GenStatusNotificationResponse.generate(
        )
        return await self._wait_for_result(Action.status_notification, default_message=default_message)

    @on(Action.stop_transaction)
    async def _on_stop_transaction_request(
        self,
        meter_stop: int,
        timestamp: str,
        transaction_id: int,
        id_tag: str | None = None,
        reason: str | Reason | None = None,
        transaction_data: list | None = None
    ) -> call_result.Authorize:
        default_message: StopTransaction = GenStopTransactionResponse.generate(
            id_tag_info=GenStartTransactionResponse.get_id_tag_info(
                status=AuthorizationStatus.invalid
            )
        )
        return await self._wait_for_result(Action.stop_transaction, default_message=default_message)

    @on(Action.trigger_message)
    async def _on_trigger_message_request(
        self,
        requested_message: str | MessageTrigger,
        connector_id: int | None = None
    ) -> call_result.Authorize:
        default_message: TriggerMessage = GenTriggerMessageResponse.generate(
            status=TriggerMessageStatus.rejected
        )
        return await self._wait_for_result(Action.trigger_message, default_message=default_message)

    @on(Action.unlock_connector)
    async def _on_unlock_connector_request(
        self,
        connector_id: int
    ) -> call_result.Authorize:
        default_message: UnlockConnector = GenUnlockConnectorResponse.generate(
            status=UnlockStatus.unlock_failed
        )
        return await self._wait_for_result(Action.unlock_connector, default_message=default_message)

    @on(Action.update_firmware)
    async def _on_update_firmware_request(
        self,
        location: str,
        retrieve_date: str,
        retries: int | None = None,
        retry_interval: int | None = None
    ) -> call_result.Authorize:
        default_message: UpdateFirmware = GenUpdateFirmwareResponse.generate(
        )
        return await self._wait_for_result(Action.update_firmware, default_message=default_message)
