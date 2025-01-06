from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class meter_values_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        evse_id: int,
        meter_value: list,
        custom_data: dict | None = None
    ) -> call.MeterValues:
        """
        生成 MeterValuesRequest

        - 参数: 
            - evse_id(int): 
                - 请求正文, EVSE ID. Numeric_ Identifier 这包含一个数字 (>0), 指定充电站的 EVSE. "0"(零)用于指定主功率计. 
            - meter_value(list): 
                - Meter_ Value MeterValuesRequest 和 TransactionEvent 中一个或多个采样值的集合. MeterValue 中的所有采样值均在同一时间点采样. 
                - 推荐使用 `get_meter_value()` 传入列表元素 或 自行创建列表.
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            evse_id=evse_id,
            meter_value=meter_value,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.MeterValues:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.MeterValues
        """
        return call.MeterValues(
            evse_id=dict_data['evseId'],
            meter_value=dict_data['meterValue'],
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
                - Base64 编码, 包含签名数据, 其中可能包含的不仅仅包含meterValue. 它可以包含时间戳、客户参考等信息. 
                - 长度范围: [1, 2500]
            - signing_method(str): 
                - 用于创建数字签名的方法. 
                - 长度范围: [1, 50]
            - encoding_method(str): 
                - 在应用数字签名算法之前对仪表值进行编码的方法. 
                - 长度范围: [1, 50]
            - public_key(str): 
                - Base64编码, 发送取决于配置变量 _PublicKeyWithSignedMeterValue_. 
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
                - 单位. 如果(默认)被测量是"能量"类型, 则默认 ="Wh". 该字段应使用第 2 部分附录中标准化测量单位列表中的值. 如果该列表中有适用的单位, 否则可能会使用"自定义"单位. 
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
