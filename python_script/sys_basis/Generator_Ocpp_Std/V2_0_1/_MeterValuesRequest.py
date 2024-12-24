
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class meter_values_request(Base_OCPP_Struct_V2_0_1): 

    @staticmethod
    def generate(evse_id: int, meter_value: list | None = None,
                 custom_data: dict | None = None, **kwargs) -> call.MeterValues:
        """
        生成 MeterValuesRequest

        参数:
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入
        - evse_id(int): evse的id.
        - meter_value(list): 推荐使用 `get_meter_value()` 传入

        返回值:
        - call.MeterValues
        """
        return call.MeterValues(
            evse_id=evse_id or kwargs.get("evse_id", None),
            meter_value=meter_value or kwargs.get("meter_value", None),
            custom_data=custom_data or kwargs.get("custom_data", None)
        )

    @staticmethod
    def get_meter_value(time_stamp: str, sampled_value: list | None = None, custom_data: dict | None = None) -> dict:
        """
        生成 MeterValue

        参数:
        - sampled_value(list): 推荐使用 `get_sampled_value_list()` 传入
        - time_stamp(str): 被测量的数值的时间戳，字符形式为"date-time"
        - custom_data(dict): 推荐使用 `get_custom_data()` 传入

        返回值:
        - meter_value
        """
        temp_dict = {
            "sampledValue": sampled_value,
            "timeStamp": time_stamp,
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_sampled_value_list(*sampled_value: dict) -> list:
        """
        生成 sampledValue列表

        参数:
        - *sampled_value(dict): 推荐使用 `get_sampled_value()` 传入

        返回值:
        - sampled_value(list)
        """
        return [*sampled_value]

    @staticmethod
    def get_sampled_value(value: float, context: str | ReadingContextType, measurand: str | MeasurandType,
                          phase: str | PhaseType, location: str | LocationType, signed_meter_value: dict,
                          unit_of_measure: dict, custom_data: dict | None = None) -> dict:
        """
        生成 SampledValue

        参数:
        - value(float): 采样值, 数值.
        - context(str|ReadingContextType): 采样值,上下文.
            - `Interruption.Begin`,`Interruption.End`,`Other`,`Sample.Clock`,`Sample.Periodic`,
            - `Transaction.Begin`,`Transaction.End`,`Trigger`.
            - 或者使用 `ReadingContextType` 枚举, 例如 `ReadingContextType.interruption.begin`.
        - measurand(str|MeasurandType): 采样值, 被测量.
            - `Current.Export`,`Current.Import`,`Current.Offered`,`Energy.Active.Export.Register`,
            - `Energy.Active.Import.Register`,`Energy.Reactive.Export.Register`,`Power.Active.Export`,`Power.Factor`,
            - `Energy.Reactive.Import.Register`,`Energy.Active.Export.Interval`,`Energy.Active.Import.Interval`,
            - `Energy.Active.Net`,`Energy.Reactive.Export.Interval`,`Energy.Reactive.Import.Interval`,,`Voltage`
            - `Energy.Reactive.Net`,`Energy.Apparent.Net`,`Energy.Apparent.Import`,`Energy.Apparent.Export`,`Frequency`,
            - `Power.Active.Import`,`Power.Offered`,`Power.Reactive.Export`,`Power.Reactive.Import`,`SoC`.
            - 或者使用 `MeasurandType` 枚举, 例如 `MeasurandType.current.export`.
        - phase(str|PhaseType): 采样值, 相位.
            - `L1`,`L2`,`L3`,`N`,`L1-N`,`L2-N`,`L3-N`,`L1-L2`,`L2-L3`,`L3-L1`.
            - 或者使用 `PhaseType` 枚举, 例如 `PhaseType.l1`.
        - location(str|LocationType): 采样值, 位置.
            - `Body`,`Cable`,`EV`,`Inlet`,`Outlet`.
            - 或者使用 `LocationType` 枚举, 例如 `LocationType.body`.
        - signed_meter_value(dict): 签过名的meterValue, 推荐使用 get_signed_meter_value() 传入
        - unit_of_measure(dict): 用乘数表示测量单位, 推荐使用 get_unit_of_measure() 传入
        - custom_data(dict): 推荐使用 get_custom_data() 传入

        返回值:
        - sampled_value(dict)
        """
        temp_dict = {
            "value": value
            }
        if context is not None:
            temp_dict["context"] = context
        if measurand is not None:
            temp_dict["measurand"] = measurand
        if phase is not None:
            temp_dict["phase"] = phase
        if location is not None:
            temp_dict["location"] = location
        if signed_meter_value is not None:
            temp_dict["signedMeterValue"] = signed_meter_value
        if unit_of_measure is not None:
            temp_dict["unitOfMeasure"] = unit_of_measure
        if custom_data is not None:
            temp_dict["customData"] = custom_data

        return temp_dict

    @staticmethod
    def get_signed_meter_value(signed_meter_data: str, signing_method: str,
                               encoding_method: str, public_key: str, custom_data: dict | None = None) -> dict:

        """
        生成 signedMeterValue

        参数:
        - signed_meter_data(str):Base64 编码，包含签名数据，这些数据可能不仅仅包含meterValue。它可能还包含诸如时间戳、客户参考等信息，字符长度为[1-2500].
        - signing_method(str): 创造电子签名的方法, 字符长度为[1-50].
        - public_key(str): Base64 编码，发送取决于变量_PublicKeyWithSignedMeterValue_的设置, 字符长度为[1-2500].
        - encoding_method(str): 在使用电子签名算法前的编码meterValue的方法, 字符长度为[1-50].
        - custom_data(dict): 推荐使用 get_custom_data() 传入
        返回值:
        - signed_meter_value(dict)
        """

        temp_dict = {
            "signedMeterData": signed_meter_data,
            "signingMethod": signing_method,
            "publicKey": public_key,
            "encodingMethod": encoding_method
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data

        return temp_dict

    @staticmethod
    def get_unit_of_measure(unit: str, multiplier: int, custom_data: dict | None = None) -> dict:

        """
        生成 UnitOfMeasure

        参数:
        - unit(str): 数值的单位, 默认是Wh, 字符长度[1-20].
        - multiplier(int): 该值表示以 10 为底的指数. 例如, 乘数为 3 表示 10 的 3 次方. 默认值为 0.
        - custom_data(dict): 推荐使用 get_custom_data() 传入
        返回值:
        - unit_of_measure(dict)
        """

        temp_dict = {
        }
        if unit is not None:
            temp_dict["unit"] = unit
        if multiplier is not None:
            temp_dict["multiplier"] = multiplier
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict
