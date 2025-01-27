
import asyncio
import time
import traceback
from datetime import datetime
from ocpp.routing import on
from ocpp.v201.call_result import *
from const.Charge_Point_Parameters import CP_Params
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v201 import ChargePoint as cpv201


class ChargePointV201(cpv201, ChargePointBase):
    """ 
    OCPP v2.0.1 信息端口类
    用于监听 ocpp 消息, 以及发送 ocpp 消息

    - 信号: 
        - signal_charge_point_ocpp_request(dict): OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        - signal_charge_point_ocpp_response(dict): OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `result`(int): 响应结果, 表示响应是否成功收到. 
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        - signal_charge_point_ocpp_response_result(dict): OCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
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

    def __init__(
        self,
        id,
        connection,
        response_timeout: int | float = 30
    ) -> None:
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()
        self._set_network_buffer_time_in_baseclass(CP_Params.NETWORK_BUFFER_TIME)
        self._set_doSendDefaultResponse(CP_Params.DO_SEND_DEFAULT_RESPONSE)

    async def send_request_message(self, message) -> None:
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
        id_token: dict,
        custom_data: dict | None = None,
        certificate: str | None = None,
        hash_data: list | None = None
    ) -> call_result.Authorize:
        default_message: Authorize = GenAuthorizeResponse.generate(
            id_token_info=GenAuthorizeResponse.get_id_token_info('Unknown')
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.authorize, default_message)

    @on(Action.boot_notification)
    async def _on_boot_notification_request(
        self,
        charging_station: dict,
        reason: str | BootReasonType,
        custom_data: dict | None = None
    ) -> call_result.BootNotification:
        default_message: BootNotification = GenBootNotificationResponse.generate(
            current_time=str(time.time()),
            interval=10,
            status=RegistrationStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.boot_notification, default_message)

    @on(Action.cancel_reservation)
    async def _on_cancel_reservation_request(
        self,
        reservation_id: int,
        custom_data: dict | None = None
    ) -> call_result.CancelReservation:
        default_message: CancelReservation = GenCancelReservationResponse.generate(
            status=CancelReservationStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.cancel_reservation, default_message)

    @on(Action.certificate_signed)
    async def _on_certificate_signed_request(
        self,
        certificate_chain: str,
        certificate_type: str | CertificateSigningUseType | None = None,
        custom_data: dict | None = None
    ) -> call_result.CertificateSigned:
        default_message: CertificateSigned = GenCertificateSignedResponse.generate(
            status=CertificateSignedStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.certificate_signed, default_message)

    @on(Action.change_availability)
    async def _on_change_availability_request(
        self,
        operational_status: str | OperationalStatusType,
        evse: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.ChangeAvailability:
        default_message: CertificateSigned = GenCertificateSignedResponse.generate(
            status=ChangeAvailabilityStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.change_availability, default_message)

    @on(Action.clear_cache)
    async def _on_clear_cache_request(
        self,
        custom_data: dict | None = None
    ) -> call_result.ClearCache:
        default_message: ClearCache = GenClearCacheResponse.generate(
            status=ClearCacheStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.clear_cache, default_message)

    @on(Action.clear_charging_profile)
    async def _on_clear_charging_profile_request(
        self,
        charging_profile_id: int | None = None,
        charging_profile_criteria: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.ClearChargingProfile:
        default_message: ClearChargingProfile = GenClearChargingProfileResponse.generate(
            status=ClearChargingProfileStatusType.unknown
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.clear_charging_profile, default_message)

    @on(Action.clear_display_message)
    async def _on_clear_display_message_request(
        self,
        id: int,
        custom_data: dict | None = None
    ) -> call_result.ClearDisplayMessage:
        default_message: ClearDisplayMessage = GenClearDisplayMessageResponse.generate(
            status=ClearMessageStatusType.unknown
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.clear_display_message, default_message)

    @on(Action.cleared_charging_limit)
    async def _on_cleared_charging_limit_request(
        self,
        charging_limit_source: str | ChargingLimitSourceType,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.ClearedChargingLimit:
        default_message: ClearedChargingLimit = GenClearedChargingLimitResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.cleared_charging_limit, default_message)

    @on(Action.clear_variable_monitoring)
    async def _on_clear_variable_monitoring_request(
        self,
        id: list,
        custom_data: dict | None = None
    ) -> call_result.ClearVariableMonitoring:
        default_message: ClearVariableMonitoring = GenClearVariableMonitoringResponse.generate(
            clear_monitoring_result=[
                GenClearVariableMonitoringResponse.get_clear_monitoring_result(
                    status=ClearMonitoringStatusType.rejected,
                    id=id
                )
            ]
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.clear_variable_monitoring, default_message)

    @on(Action.cost_updated)
    async def _on_cost_updated_request(
        self,
        total_cost: int | float,
        transaction_id: str,
        custom_data: dict | None = None
    ) -> call_result.CostUpdated:
        default_message: CostUpdated = GenCostUpdatedResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.cost_updated, default_message)

    @on(Action.customer_information)
    async def _on_customer_information_request(
        self,
        request_id: int,
        report: bool,
        clear: bool,
        customer_certificate: dict | None = None,
        id_token: dict | None = None,
        customer_identifier: str | None = None,
        custom_data: dict | None = None
    ) -> call_result.CustomerInformation:
        default_message: CustomerInformation = GenCustomerInformationResponse.generate(
            status=CustomerInformationStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.customer_information, default_message)

    @on(Action.data_transfer)
    async def _on_data_transfer_request(
        self,
        vendor_id: str,
        message_id: str | None = None,
        data=None,
        custom_data: dict | None = None
    ) -> call_result.DataTransfer:
        default_message: DataTransfer = GenDataTransferResponse.generate(
            status=DataTransferStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.data_transfer, default_message)

    @on(Action.delete_certificate)
    async def _on_delete_certificate_request(
        self,
        certificate_hash_data: dict,
        custom_data: dict | None = None
    ) -> call_result.DeleteCertificate:
        default_message: DeleteCertificate = GenDeleteCertificateResponse.generate(
            status=DeleteCertificateStatusType.failed
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.delete_certificate, default_message)

    @on(Action.firmware_status_notification)
    async def _on_firmware_status_notification_request(
        self,
        status: str | FirmwareStatusType,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.FirmwareStatusNotification:
        default_message: FirmwareStatusNotification = GenFirmwareStatusNotificationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.firmware_status_notification, default_message)

    @on(Action.get_base_report)
    async def _on_get_base_report_request(
        self,
        request_id: int,
        report_base: str | ReportBaseType,
        custom_data: dict | None = None
    ) -> call_result.GetBaseReport:
        default_message: GetBaseReport = GenGetBaseReportResponse.generate(
            status=GenericDeviceModelStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_base_report, default_message)

    @on(Action.get_certificate_status)
    async def _on_get_certificate_status_request(
        self,
        ocsp_request_data: dict,
        custom_data: dict | None = None
    ) -> call_result.GetCertificateStatus:
        default_message: GetCertificateStatus = GenGetCertificateStatusResponse.generate(
            status=GetCertificateStatusType.failed
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_certificate_status, default_message)

    @on(Action.get_charging_profiles)
    async def _on_get_charging_profiles_request(
        self,
        request_id: int,
        charging_profile: dict,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetChargingProfiles:
        default_message: GetChargingProfiles = GenGetChargingProfilesResponse.generate(
            status=GetChargingProfileStatusType.no_profiles
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_charging_profiles, default_message)

    @on(Action.get_composite_schedule)
    async def _on_get_composite_schedule_request(
        self,
        duration: int,
        evse_id: int,
        charging_rate_unit: str | ChargingRateUnitType | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetCompositeSchedule:
        default_message: GetCompositeSchedule = GenGetCompositeScheduleResponse.generate(
            status=GenericStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_composite_schedule, default_message)

    @on(Action.get_display_messages)
    async def _on_get_display_messages_request(
        self,
        request_id: int,
        id: list | None = None,
        priority: str | MessagePriorityType | None = None,
        state: str | MessageStateType | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetDisplayMessages:
        default_message: GetDisplayMessages = GenGetDisplayMessagesResponse.generate(
            status=GetDisplayMessagesStatusType.unknown
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_display_messages, default_message)

    @on(Action.get_installed_certificate_ids)
    async def _on_get_installed_certificate_ids_request(
        self,
        certificate_type: list | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetInstalledCertificateIds:
        default_message: GetInstalledCertificateIds = GenGetInstalledCertificateIdsResponse.generate(
            status=GetInstalledCertificateStatusType.notFound
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_installed_certificate_ids, default_message)

    @on(Action.get_local_list_version)
    async def _on_get_local_list_version_request(
        self,
        custom_data: dict | None = None
    ) -> call_result.GetLocalListVersion:
        default_message: GetLocalListVersion = GenGetLocalListVersionResponse.generate(
            version_number=201
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_local_list_version, default_message)

    @on(Action.get_log)
    async def _on_get_log_request(
        self,
        log: dict,
        log_type: str | LogType,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetLog:
        default_message: GetLog = GenGetLogResponse.generate(
            status=LogStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_log, default_message)

    @on(Action.get_monitoring_report)
    async def _on_get_monitoring_report_request(
        self,
        request_id: int,
        component_variable: list | None = None,
        monitoring_criteria: list | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetMonitoringReport:
        default_message: GetMonitoringReport = GenGetMonitoringReportResponse.generate(
            status=GenericDeviceModelStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_monitoring_report, default_message)

    @on(Action.get_report)
    async def _on_get_report_request(
        self,
        request_id: int,
        component_variable: list | None = None,
        component_criteria: list | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetReport:
        default_message: GetReport = GenGetReportResponse.generate(
            status=GenericDeviceModelStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_report, default_message)

    @on(Action.get_transaction_status)
    async def _on_get_transaction_status_request(
        self,
        transaction_id: str | None = None,
        custom_data: dict | None = None
    ) -> call_result.GetTransactionStatus:
        default_message: GetTransactionStatus = GenGetTransactionStatusResponse.generate(
            messages_in_queue=True
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_transaction_status, default_message)

    @on(Action.get_variables)
    async def _on_get_variables_request(
        self,
        get_variable_data: list,
        custom_data: dict | None = None
    ) -> call_result.GetVariables:
        default_message: GetVariables = GenGetVariablesResponse.generate(
            get_variable_result=[
                GenGetVariablesResponse.get_get_variable_result(attribute_status=GetVariableStatusType.rejected)
            ]
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.get_variables, default_message)

    @on(Action.heartbeat)
    async def _on_heartbeat_request(
        self,
        custom_data: dict | None = None
    ) -> call_result.Heartbeat:
        default_message: Heartbeat = GenHeartbeatResponse.generate(
            current_time=datetime.now()  # check format, there is a function in tools.data_gene.DataGene.
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.heartbeat, default_message)

    @on(Action.install_certificate)
    async def _on_install_certificate_request(
        self,
        certificate_type: str | InstallCertificateUseType,
        certificate: str,
        custom_data: dict | None = None
    ) -> call_result.InstallCertificate:
        default_message: InstallCertificate = GenInstallCertificateResponse.generate(
            status=InstallCertificateStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.install_certificate, default_message)

    @on(Action.log_status_notification)
    async def _on_log_status_notification_request(
        self,
        status: str | UploadLogStatusType,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.LogStatusNotification:
        default_message: LogStatusNotification = GenLogStatusNotificationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.log_status_notification, default_message)

    @on(Action.meter_values)
    async def _on_meter_values_request(
        self,
        evse_id: int,
        meter_value: list,
        custom_data: dict | None = None
    ) -> call_result.MeterValues:
        default_message: MeterValues = GenMeterValuesResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.meter_values, default_message)

    @on(Action.notify_charging_limit)
    async def _on_notify_charging_limit_request(
        self,
        charging_limit: dict,
        charging_schedule: list | None = None,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyChargingLimit:
        default_message: NotifyChargingLimit = GenNotifyChargingLimitResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_charging_limit, default_message)

    @on(Action.notify_customer_information)
    async def _on_notify_customer_information_request(
        self,
        data: str,
        seq_no: int,
        generated_at: str,
        request_id: int,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyCustomerInformation:
        default_message: NotifyCustomerInformation = GenNotifyCustomerInformationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_customer_information, default_message)

    @on(Action.notify_display_messages)
    async def _on_notify_display_messages_request(
        self,
        request_id: int,
        message_info: list | None = None,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyDisplayMessages:
        default_message: NotifyDisplayMessages = GenNotifyDisplayMessagesResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_display_messages, default_message)

    @on(Action.NotifyEVChargingNeeds)
    async def _on_notify_ev_charging_needs_request(
        self,
        charging_needs: dict,
        evse_id: int,
        max_schedule_tuples: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyEVChargingNeeds:
        default_message: NotifyEVChargingNeeds = GenNotifyEVChargingNeedsResponse.generate(
            status=NotifyEVChargingNeedsStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.NotifyEVChargingNeeds, default_message)

    @on(Action.notify_ev_charging_schedule)
    async def _on_notify_ev_charging_schedule_request(
        self,
        time_base: str,
        charging_schedule: dict,
        evse_id: int,
        custom_data: dict | None = None
    ) -> call_result.NotifyEVChargingSchedule:
        default_message: NotifyEVChargingSchedule = GenNotifyEVChargingScheduleResponse.generate(
            status=GenericStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_ev_charging_schedule, default_message)

    @on(Action.notify_event)
    async def _on_notify_event_request(
        self,
        generated_at: str,
        seq_no: int,
        event_data: list,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyEvent:
        default_message: NotifyEvent = GenNotifyEventResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_event, default_message)

    @on(Action.notify_monitoring_report)
    async def _on_notify_monitoring_report_request(
        self,
        request_id: int,
        seq_no: int,
        generated_at: str,
        monitor: list | None = None,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyMonitoringReport:
        default_message: NotifyMonitoringReport = GenNotifyMonitoringReportResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_monitoring_report, default_message)

    @on(Action.notify_report)
    async def _on_notify_report_request(
        self,
        request_id: int,
        generated_at: str,
        seq_no: int,
        report_data: list | None = None,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.NotifyReport:
        default_message: NotifyReport = GenNotifyReportResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.notify_report, default_message)

    @on(Action.publish_firmware)
    async def _on_publish_firmware_request(
        self,
        location: str,
        checksum: str,
        request_id: int,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.PublishFirmware:
        default_message: PublishFirmware = GenPublishFirmwareResponse.generate(
            status=GenericStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.publish_firmware, default_message)

    @on(Action.publish_firmware_status_notification)
    async def _on_publish_firmware_status_notification_request(
        self,
        status: str | PublishFirmwareStatusType,
        location: list | None = None,
        request_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.PublishFirmwareStatusNotification:
        default_message: PublishFirmwareStatusNotification = GenPublishFirmwareStatusNotificationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.publish_firmware_status_notification, default_message)

    @on(Action.report_charging_profiles)
    async def _on_report_charging_profiles_request(
        self,
        request_id: int,
        charging_limit_source: str | ChargingLimitSourceType,
        charging_profile: list,
        evse_id: int,
        tbc: bool | None = None,
        custom_data: dict | None = None
    ) -> call_result.ReportChargingProfiles:
        default_message: ReportChargingProfiles = GenReportChargingProfilesResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.report_charging_profiles, default_message)

    @on(Action.request_start_transaction)
    async def _on_request_start_transaction_request(
        self,
        id_token: dict,
        remote_start_id: int,
        evse_id: int | None = None,
        group_id_token: dict | None = None,
        charging_profile: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.RequestStartTransaction:
        default_message: RequestStartTransaction = GenRequestStartTransactionResponse.generate(
            status=RequestStartStopStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.request_start_transaction, default_message)

    @on(Action.request_stop_transaction)
    async def _on_request_stop_transaction_request(
        self,
        transaction_id: str,
        custom_data: dict | None = None
    ) -> call_result.RequestStopTransaction:
        default_message: RequestStopTransaction = GenRequestStopTransactionResponse.generate(
            status=RequestStartStopStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.request_stop_transaction, default_message)

    @on(Action.reservation_status_update)
    async def _on_reservation_status_update_request(
        self,
        reservation_id: int,
        reservation_update_status: str | ReservationUpdateStatusType,
        custom_data: dict | None = None
    ) -> call_result.ReservationStatusUpdate:
        default_message: ReservationStatusUpdate = GenReservationStatusUpdateResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.reservation_status_update, default_message)

    @on(Action.reserve_now)
    async def _on_reserve_now_request(
        self,
        id: int,
        expiry_date_time: str,
        id_token: dict,
        connector_type: str | ConnectorType | None = None,
        evse_id: int | None = None,
        group_id_token: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.ReserveNow:
        default_message: ReserveNow = GenReserveNowResponse.generate(
            status=ReserveNowStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.reserve_now, default_message)

    @on(Action.reset)
    async def _on_reset_request(
        self,
        type: str | ResetType,
        evse_id: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.Reset:
        default_message: Reset = GenResetResponse.generate(
            status=ResetStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.reset, default_message)

    @on(Action.security_event_notification)
    async def _on_security_event_notification_request(
        self,
        type: str,
        timestamp: str,
        tech_info: str | None = None,
        custom_data: dict | None = None
    ) -> call_result.SecurityEventNotification:
        default_message: SecurityEventNotification = GenSecurityEventNotificationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.security_event_notification, default_message)

    @on(Action.send_local_list)
    async def _on_send_local_list_request(
        self,
        version_number: int,
        update_type: str | UpdateType,
        local_authorization_list: list | None = None,
        custom_data: dict | None = None
    ) -> call_result.SendLocalList:
        default_message: SendLocalList = GenSendLocalListResponse.generate(
            status=SendLocalListStatusType.failed
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.send_local_list, default_message)

    @on(Action.SetChargingProfile)
    async def _on_set_charging_profile_request(
        self,
        evse_id: int,
        charging_profile: dict,
        custom_data: dict | None = None
    ) -> call_result.SetChargingProfile:
        default_message: SetChargingProfile = GenSetChargingProfileResponse.generate(
            status=ChargingProfileStatus.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.SetChargingProfile, default_message)

    @on(Action.set_display_message)
    async def _on_set_display_message_request(
        self,
        message: dict,
        custom_data: dict | None = None
    ) -> call_result.SetDisplayMessage:
        default_message: SetDisplayMessage = GenSetDisplayMessageResponse.generate(
            status=DisplayMessageStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_display_message, default_message)

    @on(Action.set_monitoring_base)
    async def _on_set_monitoring_base_request(
        self,
        monitoring_base: str | MonitorBaseType,
        custom_data: dict | None = None
    ) -> call_result.SetMonitoringBase:
        default_message: SetMonitoringBase = GenSetMonitoringBaseResponse.generate(
            status=GenericDeviceModelStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_monitoring_base, default_message)

    @on(Action.set_monitoring_level)
    async def _on_set_monitoring_level_request(
        self,
        severity: int,
        custom_data: dict | None = None
    ) -> call_result.SetMonitoringLevel:
        default_message: SetMonitoringLevel = GenSetMonitoringLevelResponse.generate(
            status=GenericStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_monitoring_level, default_message)

    @on(Action.set_network_profile)
    async def _on_set_network_profile_request(
        self,
        configuration_slot: int,
        connection_data: dict,
        custom_data: dict | None = None
    ) -> call_result.SetNetworkProfile:
        default_message: SetNetworkProfile = GenSetNetworkProfileResponse.generate(
            status=SetNetworkProfileStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_network_profile, default_message)

    @on(Action.set_variable_monitoring)
    async def _on_set_variable_monitoring_request(
        self,
        set_monitoring_data: list,
        custom_data: dict | None = None
    ) -> call_result.SetVariableMonitoring:
        default_message: SetVariableMonitoring = GenSetVariableMonitoringResponse.generate(
            set_monitoring_result=[]
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_variable_monitoring, default_message)

    @on(Action.set_variables)
    async def _on_set_variables_request(
        self,
        set_variable_data: list,
        custom_data: dict | None = None
    ) -> call_result.SetVariables:
        default_message: SetVariables = GenSetVariablesResponse.generate(
            set_variable_result=[]
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.set_variables, default_message)

    @on(Action.sign_certificate)
    async def _on_sign_certificate_request(
        self,
        csr: str,
        certificate_type: str | CertificateSigningUseType | None = None,
        custom_data: dict | None = None
    ) -> call_result.SignCertificate:
        default_message: SignCertificate = GenSignCertificateResponse.generate(
            status=GenericStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.sign_certificate, default_message)

    @on(Action.status_notification)
    async def _on_status_notification_request(
        self,
        timestamp: str,
        connector_status: str | ConnectorStatusType,
        evse_id: int,
        connector_id: int,
        custom_data: dict | None = None
    ) -> call_result.StatusNotification:
        default_message: StatusNotification = GenStatusNotificationResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.status_notification, default_message)

    @on(Action.transaction_event)
    async def _on_transaction_event_request(
        self,
        event_type: str | TransactionEventType,
        timestamp: str,
        trigger_reason: str | TriggerReasonType,
        seq_no: int,
        transaction_info: dict,
        custom_data: dict | None = None,
        meter_value: list | None = None,
        offline: bool = False,
        number_of_phases_used: int | None = None,
        cable_max_current: int | None = None,
        reservation_id: int | None = None,
        evse: dict | None = None,
        id_token: dict | None = None
    ) -> call_result.TransactionEvent:
        default_message: TransactionEvent = GenTransactionEventResponse.generate(
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.transaction_event, default_message)

    @on(Action.trigger_message)
    async def _on_trigger_message_request(
        self,
        requested_message: str | MessageTriggerType,
        evse: dict | None = None,
        custom_data: dict | None = None
    ) -> call_result.TriggerMessage:
        default_message: TriggerMessage = GenTriggerMessageResponse.generate(
            status=TriggerMessageStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.trigger_message, default_message)

    @on(Action.unlock_connector)
    async def _on_unlock_connector_request(
        self,
        evse_id: int,
        connector_id: int,
        custom_data: dict | None = None
    ) -> call_result.UnlockConnector:
        default_message: UnlockConnector = GenUnlockConnectorResponse.generate(
            status=UnlockStatusType.unlock_failed
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.unlock_connector, default_message)

    @on(Action.unpublish_firmware)
    async def _on_unpublish_firmware_request(
        self,
        checksum: str,
        custom_data: dict | None = None
    ) -> call_result.UnpublishFirmware:
        default_message: UnpublishFirmware = GenUnpublishFirmwareResponse.generate(
            status=UnpublishFirmwareStatusType.no_firmware
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.unpublish_firmware, default_message)

    @on(Action.update_firmware)
    async def _on_update_firmware_request(
        self,
        request_id: int,
        firmware: dict,
        retries: int | None = None,
        retry_interval: int | None = None,
        custom_data: dict | None = None
    ) -> call_result.UpdateFirmware:
        default_message: UpdateFirmware = GenUpdateFirmwareResponse.generate(
            status=UpdateFirmwareStatusType.rejected
        )
        wait_for_result = await self._wait_for_result_func()
        return await wait_for_result(Action.update_firmware, default_message)
