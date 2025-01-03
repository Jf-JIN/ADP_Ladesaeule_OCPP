
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class transaction_event_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(event_type: str | TransactionEventType,
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
                 id_token: dict | None = None,
                 **kwargs) -> call.TransactionEvent:
        """
        生成 TransactionEventRequest

        参数:
            - event_type(str|TransactionEventType): 时间的类型
                - 字符串, 无先后顺序和分组, 仅是逻辑分组: `Ended`,`Started`,`Updated`.
            - timestamp(str): 交易时间出现的日期和时间, 字符串, 格式为"date-time".
            - trigger_reason(str|TriggerReasonType):充电桩向CSMS发送此消息的原因.
                - 字符串, 无先后顺序和分组, 仅是逻辑分组:
                    - `Authorized`,`CablePluggedIn`,`ChargingRateChanged`,`ChargingStateChanged`,`Deauthorized`,`EnergyLimitReached`,`EVCommunicationLost`,
                    - `EVConnectTimeout`,`MeterValueClock`,`MeterValuePeriodic`,`TimeLimitReached`,`Trigger`,`UnlockCommand`,`StopAuthorized`,`EVDeparted`,`EVDetected`,`RemoteStop`,
                    - `RemoteStart`,`AbnormalCondition`,`SignedDataReceived`,`ResetCommand`
            - seq_no(int): 递增的序列号, 有助于确定是否已接收到交易的所有消息.
            - transaction_info(dict): 交易, 推荐使用`get_transaction_info()` 传入
            - custom_data(dict):推荐使用 `get_custom_data()` 传入
            - meter_value(list): 推荐使用 `get_meter_value_list()` 传入
            - offline(bool): 表示此交易事件是否发生在充电站离线时.默认值为 false, 表示该事件发生在充电站在线时.
            - number_of_phases_used(int): 如果充电站能够报告使用的相位数量, 则必须提供该信息.如果未提供, CSMS(充电站管理系统)可能能够通过设备管理确定使用的相位数量.
            - cable_max_current(int): 连接线束中最大电流值, 单位为A.
            - reservation_id(int): 终止此次交易的预约id.
            - evse(dict): 推荐使用 `get_evse()` 传入
            - id_token(dict): 推荐使用 `get_id_tocken()` 传入

        返回值:
            - call.TransactionEvent
        """
        return call.TransactionEvent(
            event_type=event_type or kwargs.get("event_type"),
            timestamp=timestamp or kwargs.get("timestamp"),
            trigger_reason=trigger_reason or kwargs.get("trigger_reason"),
            seq_no=seq_no or kwargs.get("seq_no"),
            transaction_info=transaction_info or kwargs.get("transaction_info"),
            custom_data=custom_data or kwargs.get("custom_data", None),
            meter_value=meter_value or kwargs.get("meter_value", None),
            offline=offline or kwargs.get("offline", None),
            number_of_phases_used=number_of_phases_used or kwargs.get("number_of_phases_used", None),
            cable_max_current=cable_max_current or kwargs.get("cable_max_current", None),
            reservation_id=reservation_id or kwargs.get("reservation_id", None),
            evse=evse or kwargs.get("evse", None),
            id_token=id_token or kwargs.get("id_token", None),
        )

    @staticmethod
    def get_meter_value_list(*meter_value: dict) -> list:
        """
        生成 meterValue列表

        参数:
            - *meter_value(dict): 推荐使用 `get_meter_value()` 传入, 最少一项, 无上限

        返回值:
            - meter_value(list)
        """
        return [*meter_value]

    @staticmethod
    def get_meter_value(time_stamp: str, sampled_value: list, custom_data: dict | None = None) -> dict:
        """
        生成 MeterValue

        参数:
            - sampled_value(list): 推荐使用 `get_sampled_value_list()` 传入
            - time_stamp(str): 被测量的数值的时间戳, 字符形式为"date-time"
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - meter_value(dict)
        """
        temp_dict = {
            "sampledValue": sampled_value,
            "timeStamp": time_stamp,
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_transaction_info(transaction_id: str, charging_state: str | ChargingStateType, time_spent_charging: int, stopped_reason: str | ReasonType, remote_start_id: int, custom_data: dict | None = None) -> dict:
        """
        生成 transactionInfo

        参数:
            - transaction_id(str): 交易的id, 字符串长度为[1-36]
            - charging_state(str|ChargingStateType): 交易状态, `Charging`,`EVConnected`,`SuspendedEV`,`SuspendedEVSE`,`Idle`
            - time_spent_charging(int): 在交易过程中从 EVSE向 EV(电动车)传输能量的总时间(以秒为单位). 请注意, timeSpentCharging(充电时间)小于或等于交易的持续时间.
            - stopped_reason(str|ReasonType): 交易结束原因,
                - 字符串, 无先后顺序和分组, 仅是逻辑分组:
                     -`DeAuthorized`,`EmergencyStop`,`EnergyLimitReached`,`EVDisconnected`,`GroundFault`,`ImmediateReset`,
                     -`Local`,`LocalOutOfCredit`,`MasterPass`,`Other`,`OvercurrentFault`,`PowerLoss`,`PowerQuality`,
                     -`Reboot`,`Remote`,`SOCLimitReached`,`StoppedByEV`,`TimeLimitReached`,`Timeout`
            - remote_startId(int): 分配给远程启动请求的 ID.
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
            - transaction_info(dict)
        """

        temp_dict = {
            "transactionId": transaction_id,
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if charging_state is not None:
            temp_dict["chargingState"] = charging_state
        if time_spent_charging is not None:
            temp_dict["timeSpentCharging"] = time_spent_charging
        if stopped_reason is not None:
            temp_dict["stoppedReason"] = stopped_reason
        if remote_start_id is not None:
            temp_dict["remoteStartId"] = remote_start_id
        return temp_dict

    @staticmethod
    def get_evse(evse_id: int, connector_id: int | None = None, custom_data: dict | None = None) -> dict:
        """
        生成 evse

        参数:
            - evse_id(int): evse的id.
            - connector_id(int): connector的id.
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        """

        temp_dict = {
            "evseId": evse_id,
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if connector_id is not None:
            temp_dict["connectorId"] = connector_id
        return temp_dict

    @staticmethod
    def get_id_tocken(id_token: str, id_token_type: str | IdTokenType, custom_data: dict | None = None,
                      additional_info: dict | None = None) -> dict:
        """
        生成 IdToken

        参数:
            - id_token(str): id令牌, 长度为 [1-36] 个字符
            - id_token_type(str|IdTokenType): 类型 候选:
                - `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization` .
                - 或者可以使用 `IdTokenType` 枚举, 例如: `IdTokenType.central` .
            - custom_data(dict): 推荐使用 `get_custom_data()` 传入
            - additional_info(list): 推荐使用 `get_additional_info_list()` 传入

        返回值:
            - id_tocken(dict)
        """
        temp_dict = {
            "idToken": id_token,
            "idTokenType": id_token_type
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if additional_info is not None:
            temp_dict["additionalInfo"] = additional_info
        return temp_dict

