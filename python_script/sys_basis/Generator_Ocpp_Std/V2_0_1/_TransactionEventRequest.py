from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenTransactionEventRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        event_type: str | TransactionEventType,
        timestamp: str,
        trigger_reason: str | TriggerReasonType,
        seq_no: int,
        transaction_info: dict,
        meter_value: list | None = None,
        offline: bool | None = None,
        number_of_phases_used: int | None = None,
        cable_max_current: int | None = None,
        reservation_id: int | None = None,
        evse: dict | None = None,
        id_token: dict | None = None,
        custom_data: dict | None = None
    ) -> call.TransactionEvent:
        """
        生成 TransactionEventRequest

        - 参数: 
            - event_type(str): 
                - 这包含此事件的类型. 事务的第一个 TransactionEvent 应包含: "开始" 事务的最后一个 TransactionEvent 应包含: "结束" 所有其他事务应包含: "更新" 
                - 枚举值: `Ended`, `Started`, `Updated`
                - 或使用枚举类(推荐)`TransactionEventType`. e.g. `TransactionEventType.ended`
            - timestamp(str): 
                - 该交易事件发生的日期和时间. 
                - 格式: date-time
            - trigger_reason(str): 
                - Reason the Charging Station sends this message to the CSMS 
                - 枚举值: `Authorized`, `CablePluggedIn`, `ChargingRateChanged`, `ChargingStateChanged`, `Deauthorized`, `EnergyLimitReached`, `EVCommunicationLost`, `EVConnectTimeout`, `MeterValueClock`, `MeterValuePeriodic`, `TimeLimitReached`, `Trigger`, `UnlockCommand`, `StopAuthorized`, `EVDeparted`, `EVDetected`, `RemoteStop`, `RemoteStart`, `AbnormalCondition`, `SignedDataReceived`, `ResetCommand`
                - 或使用枚举类(推荐)`TriggerReasonType`. e.g. `TriggerReasonType.authorized`
            - seq_no(int): 
                - 增量序列号, 有助于确定是否已收到事务的所有消息. 
            - transaction_info(dict): 
                - 交易
                - 推荐使用 `get_transaction_info()` 传入
            - meter_value(list|None): 
                - MeterValuesRequest 和 TransactionEvent 中一个或多个采样值的集合. MeterValue 中的所有采样值均在同一时间点采样. 
                - 推荐使用 `get_meter_value()` 传入列表元素 或 自行创建列表.
            - offline(bool|None): 
                - 表示此交易事件是否发生在充电站离线时.默认值为 false, 表示该事件发生在充电站在线时
            - number_of_phases_used(int|None): 
                - 如果充电站能够报告使用的相位数量, 则必须提供该信息.如果未提供, CSMS(充电站管理系统)可能能够通过设备管理确定使用的相位数量. 
            - cable_max_current(int|None): 
                - 连接线束中最大电流值, 单位为A.
            - reservation_id(int|None): 
                - 终止此次交易的预约id. 
            - evse(dict|None): 
                - EVSE电动汽车供电设备 
                - 推荐使用 `get_evse()` 传入
            - id_token(dict|None): 
                - 包含用于授权的不区分大小写的标识符以及支持多种形式的标识符的授权类型. 
                - 推荐使用 `get_id_token()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.TransactionEvent
        """
        return call.TransactionEvent(
            event_type=event_type,
            timestamp=timestamp,
            trigger_reason=trigger_reason,
            seq_no=seq_no,
            transaction_info=transaction_info,
            meter_value=meter_value,
            offline=offline,
            number_of_phases_used=number_of_phases_used,
            cable_max_current=cable_max_current,
            reservation_id=reservation_id,
            evse=evse,
            id_token=id_token,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.TransactionEvent:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.TransactionEvent
        """
        return call.TransactionEvent(
            event_type=dict_data['eventType'],
            timestamp=dict_data['timestamp'],
            trigger_reason=dict_data['triggerReason'],
            seq_no=dict_data['seqNo'],
            transaction_info=dict_data['transactionInfo'],
            meter_value=dict_data.get('meterValue', None),
            offline=dict_data.get('offline', None),
            number_of_phases_used=dict_data.get('numberOfPhasesUsed', None),
            cable_max_current=dict_data.get('cableMaxCurrent', None),
            reservation_id=dict_data.get('reservationId', None),
            evse=dict_data.get('evse', None),
            id_token=dict_data.get('idToken', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_signed_meter_value(
        signed_meter_data: str,
        signing_method: str,
        encoding_method: str,
        public_key: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 signed meter value

        - 参数: 
            - signed_meter_data(str): 
                - Base64 编码, 包含签名数据, 其中可能包含的不仅仅是计量值. 它可以包含时间戳、客户参考等信息. 
                - 长度范围: [1, 2500]
            - signing_method(str): 
                - 用于创建数字签名的方法. 
                - 长度范围: [1, 50]
            - encoding_method(str): 
                - 在应用数字签名算法之前对仪表值进行编码的方法. 
                - 长度范围: [1, 50]
            - public_key(str): 
                - Base64编码, 发送取决于配置变量_PublicKeyWithSignedMeterValue_. 
                - 长度范围: [1, 2500]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'signedMeterData': signed_meter_data,
            'signingMethod': signing_method,
            'encodingMethod': encoding_method,
            'publicKey': public_key
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_unit_of_measure(
        unit: str | None = None,
        multiplier: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 unit of measure

        - 参数: 
            - unit(str|None): 
                - 值的单位. 如果(默认)被测量是"能量"类型, 则默认 ="Wh". 该字段应使用第 2 部分附录中标准化测量单位列表中的值. 如果该列表中有适用的单位, 否则可能会使用"自定义"单位. 
                - 长度范围: [1, 20]
            - multiplier(int|None): 
                - 乘数, 该值表示以 10 为底的指数. 即乘数 3 表示 10 的 3 次方. 默认值为 0. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {

        }
        if unit is not None:
            temp_dict['unit'] = unit
        if multiplier is not None:
            temp_dict['multiplier'] = multiplier
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_sampled_value(
        value: int | float,
        context: str | ReadingContextType | None = None,
        measurand: str | MeasurandType | None = None,
        phase: str | PhaseType | None = None,
        location: str | LocationType | None = None,
        signed_meter_value: dict | None = None,
        unit_of_measure: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 sampled value

        - 参数: 
            - value(int|float): 
                - 采样值. 测量值. 
            - context(str||None): 
                - 上下文类型. Reading_Context_Code 详细值类型: 开始、结束或样本. 默认值=`ReadingContextType.sample_periodic`
                - 枚举值: `Interruption.Begin`, `Interruption.End`, `Other`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`
                - 或使用枚举类(推荐)`ReadingContextType`. e.g. `ReadingContextType.interruption.begin`
            - measurand(str||None): 
                - 测量类型, 默认值为 MeasurandType.energy_active_import_register 
                - 枚举值: `Current.Export`, `Current.Import`, `Current.Offered`, `Energy.Active.Export.Register`, `Energy.Active.Import.Register`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Register`, `Energy.Active.Export.Interval`, `Energy.Active.Import.Interval`, `Energy.Active.Net`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Import.Interval`, `Energy.Reactive.Net`, `Energy.Apparent.Net`, `Energy.Apparent.Import`, `Energy.Apparent.Export`, `Frequency`, `Power.Active.Export`, `Power.Active.Import`, `Power.Factor`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `SoC`, `Voltage`
                - 或使用枚举类(推荐)`MeasurandType`. e.g. `MeasurandType.current.export`
            - phase(str||None): 
                - 相位, 指示如何解释测量值. 例如, L1 和中性线之间 (L1-N). 请注意, 并非所有相位值都适用于所有被测量. 当不存在相位时, 测量值被解释为整体值. 
                - 枚举值: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1`
                - 或使用枚举类(推荐)`PhaseType`. e.g. `PhaseType.l1`
            - location(str||None): 
                - S指示测量值的采样位置, 默认值为 `LocationType.outlet`
                - 枚举值: `Body`, `Cable`, `EV`, `Inlet`, `Outlet`
                - 或使用枚举类(推荐)`LocationType`. e.g. `LocationType.body`
            - signed_meter_value(dict|None): 
                - 表示计量值的有符号版本. 
                - 推荐使用 `get_signed_meter_value()` 传入
            - unit_of_measure(dict|None): 
                - 表示带有乘数的测量单位 
                - 推荐使用 `get_unit_of_measure()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'value': value
        }
        if context is not None:
            temp_dict['context'] = context
        if measurand is not None:
            temp_dict['measurand'] = measurand
        if phase is not None:
            temp_dict['phase'] = phase
        if location is not None:
            temp_dict['location'] = location
        if signed_meter_value is not None:
            temp_dict['signedMeterValue'] = signed_meter_value
        if unit_of_measure is not None:
            temp_dict['unitOfMeasure'] = unit_of_measure
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_meter_value(
        sampled_value: list,
        timestamp: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 meter value

        - 参数: 
            - sampled_value(list): 
                - Sampled_ Value MeterValues 中的单个采样值. 每个值都可以附有可选字段. 为了节省移动数据使用量, 所有可选字段的默认值都是这样的. 没有任何附加字段的值将被解释为以 Wh(瓦时)为单位的有效输入能量的寄存器读数. 
                - 推荐使用 `get_sampled_value()` 传入列表元素 或 自行创建列表.
            - timestamp(str): 
                - 被测量的数值的时间戳(s). 
                - 格式: date-time
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'sampledValue': sampled_value,
            'timestamp': timestamp
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_transaction_info(
        transaction_id: str,
        charging_state: str | ChargingStateType | None = None,
        time_spent_charging: int | None = None,
        stopped_reason: str | ReasonType | None = None,
        remote_start_id: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 transaction info

        - 参数: 
            - transaction_id(str): 
                - 交易的id. 
                - 长度范围: [1, 36]
            - charging_state(str||None): 
                - 交易状态. 
                - 枚举值: `Charging`, `EVConnected`, `SuspendedEV`, `SuspendedEVSE`, `Idle`
                - 或使用枚举类(推荐)`ChargingStateType`. e.g. `ChargingStateType.charging`
            - time_spent_charging(int|None): 
                - 在交易过程中从 EVSE向 EV(电动车)传输能量的总时间(以秒为单位). 请注意, timeSpentCharging(充电时间)小于或等于交易的持续时间.. 
            - stopped_reason(str||None): 
                - 交易结束原因, 仅当 Reason 为"Local"时才可以省略. 
                - 枚举值: `DeAuthorized`, `EmergencyStop`, `EnergyLimitReached`, `EVDisconnected`, `GroundFault`, `ImmediateReset`, `Local`, `LocalOutOfCredit`, `MasterPass`, `Other`, `OvercurrentFault`, `PowerLoss`, `PowerQuality`, `Reboot`, `Remote`, `SOCLimitReached`, `StoppedByEV`, `TimeLimitReached`, `Timeout`
                - 或使用枚举类(推荐)`ReasonType`. e.g. `ReasonType.de_authorized`
            - remote_start_id(int|None): 
                - 为远程启动请求提供的 ID (<<requeststarttransactionrequest, RequestStartTransactionRequest>>. 这使 CSMS 能够将已启动的事务与给定的启动请求进行匹配. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'transactionId': transaction_id
        }
        if charging_state is not None:
            temp_dict['chargingState'] = charging_state
        if time_spent_charging is not None:
            temp_dict['timeSpentCharging'] = time_spent_charging
        if stopped_reason is not None:
            temp_dict['stoppedReason'] = stopped_reason
        if remote_start_id is not None:
            temp_dict['remoteStartId'] = remote_start_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_evse(
        id: int,
        connector_id: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 evse

        - 参数: 
            - id(int): 
                - Id号, MRID. Identifier EVSE 标识符. 其中包含指定充电站 EVSE 的数字 (> 0).
            - connector_id(int|None): 
                - 通过连接器索引号指定特定连接器(在 EVSE 上)的 ID. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id
        }
        if connector_id is not None:
            temp_dict['connectorId'] = connector_id
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_additional_info(
        additional_id_token: str,
        type: str,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 additional info

        - 参数: 
            - additional_id_token(str): 
                - 该字段指定附加的IdToken. 
                - 长度范围: [1, 36]
            - type(str): 
                - 这定义了additionalIdToken的类型. 这是自定义类型, 因此实现需要所有相关方都同意. 
                - 长度范围: [1, 50]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'additionalIdToken': additional_id_token,
            'type': type
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_id_token(
        id_token: str,
        type: str | IdTokenType,
        additional_info: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 id token

        - 参数: 
            - id_token(str): 
                - IdToken 不区分大小写. 可能包含 RFID 标签的隐藏 ID, 但也可以包含 UUID. 
                - 长度范围: [1, 36]
            - type(str): 
                - 枚举可能的 idToken 类型. 
                - 枚举值: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`
                - 或使用枚举类(推荐)`IdTokenType`. e.g. `IdTokenType.central`
            - additional_info(list|None): 
                - 包含用于授权的不区分大小写的标识符以及支持多种形式的标识符的授权类型. 
                - 推荐使用 `get_additional_info()` 传入列表元素 或 自行创建列表.
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'idToken': id_token,
            'type': type
        }
        if additional_info is not None:
            temp_dict['additionalInfo'] = additional_info
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
