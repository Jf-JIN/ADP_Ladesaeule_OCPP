
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_charging_profile_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        evse_id: int,
        charging_profile: dict,
        custom_data: dict | None = None
    ) -> call.SetChargingProfile:
        """
        生成 SetChargingProfileRequest

        参数:
            - evse_id: EVSE的ID
                - 对于 TxDefaultProfile, evseId=0 会将配置文件应用于每个单独的 evse. 
                - 对于 ChargingStationMaxProfile 和 ChargingStationExternalConstraints, evseId=0 包含整个充电站的总体限制
            - charging_profile: ChargingProfile 由 ChargingSchedule 组成, 描述每个时间间隔可以提供的电量或电流量. 推荐使用 `get_charging_profile` 方法
            - custom_data: 自定义数据, 推荐使用 `get_custom_data` 方法

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            evse_id=evse_id,
            charging_profile=charging_profile,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetChargingProfile:
        """
        加载字典数据, 将字典转换为数据类

        参数:
            - dict_data(dict): 字典数据

        返回值:
            - call.SetChargingProfile
        """
        return call.SetChargingProfile(
            evse_id=dict_data['evseId'],
            charging_profile=dict_data['chargingProfile'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_charging_profile(
        id: int,
        stack_level: int,
        charging_profile_purpose: str | ChargingProfilePurposeType,
        charging_profile_kind: str | ChargingProfileKindType,
        charging_schedule: list,
        recurrency_kind: str | RecurrencyKindType | None = None,
        valid_from: str | None = None,
        valid_to: str | None = None,
        transaction_id: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        ChargingProfile 由 ChargingSchedule 组成, 描述每个时间间隔可以提供的电量或电流量.

        参数:
            - id: ChargingProfile 的唯一标识符
            - stack_level: 确定配置文件层次结构堆栈中级别的值. 较高的值优先于较低的值. 最低级别为 0.
            - charging_profile_purpose: 配置文件的目的. 这决定了配置文件如何被解释.
                - `ChargingStationExternalConstraints` `ChargingStationMaxProfile` `TxDefaultProfile` `TxProfile`
                - 推荐使用 `ChargingProfilePurposeType` 枚举类型, 例如 `ChargingProfilePurposeType.tx_profile`
            - charging_profile_kind: 表示日程表的种类
                - `Absolute` `Recurring` `Relative`
                - 推荐使用 `ChargingProfileKindType` 枚举类型, 例如 `ChargingProfileKindType.absolute`
            - charging_schedule: 推荐使用 get_charging_schedule_list 方法, 最少1条, 最多3条
            - recurrency_kind: 指示重复的起点
                - `Daily` `Weekly`
                - 推荐使用 `RecurrencyKindType` 枚举类型, 例如 `RecurrencyKindType.daily`
            - valid_from: 配置文件开始生效的时间点. 如果不存在, 则配置文件在充电站收到后立即生效. 格式date-time
            - valid_to: 配置文件停止有效的时间点. 如果不存在, 则该配置文件一直有效, 直到被另一个配置文件替换为止. 格式date-time
            - transaction_id: 仅当 ChargingProfilePurpose 设置为 TxProfile 时才应包含在内.  transactionId 用于将配置文件与特定交易进行匹配. 长度 [0, 36]
            - custom_data: 自定义数据, 推荐使用 `get_custom_data` 方法

        返回值:
            - charging_profile(dict)

        """
        temp = {
            'id': id,
            'stackLevel': stack_level,
            'chargingProfilePurpose': charging_profile_purpose,
            'chargingProfileKind': charging_profile_kind,
            'charging_schedule': charging_schedule
        }
        if recurrency_kind is not None:
            temp['recurrencyKind'] = recurrency_kind
        if valid_from is not None:
            temp['validFrom'] = valid_from
        if valid_to is not None:
            temp['validTo'] = valid_to
        if transaction_id is not None:
            temp['transactionId'] = transaction_id
        if custom_data is not None:
            temp['customData'] = custom_data
        return temp

    @staticmethod
    def get_charging_schedule_list(*args) -> list:
        """
        生成 charging Schedule List

        参数:
            - 多项(dict): 推荐使用 `get_charging_schedule` 方法, 参数个数范围为 [1, 1024]

        返回值:
            - charging_schedule_list(list)
        """
        return [*args]

    @staticmethod
    def get_charging_schedule(
        id: int,
        charging_rate_unit: ChargingRateUnitType | str,
        charging_schedule_period: list,
        start_schedule: str | None = None,
        duration: int | None = None,
        min_charging_rate: float | None = None,
        sales_tariff: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 Charging Schedule

        参数:
            - id(int): 充电计划表的标识
            - charging_rate_unit(str): 充电速率单位, 直接使用ChargingRateUnitType枚举类或者自选: `W`, `A`
            - charging_schedule_period(list): 充电计划表周期, 推荐使用 `get_charging_schedule_period_list()` 传入
            - start_schedule(str): 充电计划表的绝对起始时间, 如果缺失, 则等同于充电开始时间
            - duration(int): 充电计划表持续时间(单位: 秒), 如果缺失, 最后一个周期将无限循环, 直到交易结束
            - min_charging_rate(float): 电动汽车支持的最小充电速率
            - sales_tariff(dict): 电费套餐, 推荐使用 `get_sales_tariff()` 传入
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - charging_schedule(dict)
        """
        temp_dict = {
            "id": id,
            "chargingRateUnit": charging_rate_unit,
            "chargingSchedulePeriod": charging_schedule_period
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if start_schedule is not None:
            temp_dict["startSchedule"] = start_schedule
        if duration is not None:
            temp_dict["duration"] = duration
        if min_charging_rate is not None:
            temp_dict["minChargingRate"] = min_charging_rate
        if sales_tariff is not None:
            temp_dict["salesTariff"] = sales_tariff
        return temp_dict

    @staticmethod
    def get_charging_schedule_period_list(*args) -> list:
        """
        生成 Charging Schedule Period 列表
        Charging Schedule结构 定义了充电周期列表, 如在 GetCompositeSchedule.conf 和 ChargingProfile 中使用的

        参数: 
            - 多项(list): 推荐使用 `get_charging_schedule_period()` 传入, 参数个数范围为 [1, 1024]

        返回值:
            - charging_schedule_period_list(list)
        """
        return [*args]

    @staticmethod
    def get_charging_schedule_period(start_period: int, limit: float, custom_data: dict | None = None, number_phases: int | None = None, phase_to_use: int | None = None) -> dict:
        """
        生成 Charging Schedule Period
        充电计划结构定义了充电周期列表, 如在 GetCompositeSchedule.conf 和 ChargingProfile 中使用的

        参数:
            - startPeriod(int): 充电计划表的周期开始时间, 也代表了上一周期的结束时间(单位: 秒)
            - limit(float): 计划期间的充电速率限制, 最多接受1位小数, 如8.1
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
            - number_phases(int): 充电可使用的相数, 如果需要但没有, 默认为3
            - phase_to_use(int): 仅在numberPhases=1并且EVSE能够切换连接到EV的相位, 即 ACPhaseSwitchingSupported已定义且为true的情况下使用

        返回值:
            - charging_schedule_period(dict)
        """
        temp_dict = {
            "startPeriod": start_period,
            "limit": limit
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if number_phases is not None:
            temp_dict["numberPhases"] = number_phases
        if phase_to_use is not None:
            temp_dict["phaseToUse"] = phase_to_use
        return temp_dict

    @staticmethod
    def get_sales_tariff(id: int, sales_tariff_entry: list, custom_data: dict | None = None, sales_tariff_description: str | None = None, num_ePrice_levels: int | None = None) -> dict:
        """
        生成 Sales Tariff

        参数:
            - id(int): 电费套餐的标识
            - sales_tariff_entry(list): 电费套餐条目, 最少1条, 最多1024条, 推荐使用 `get_sales_tariff_entry_list()` 传入
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
            - sales_tariff_description(str): 电费套餐的描述, 最大长度为32
            - num_ePrice_levels(int): 电费套餐条目中涉及的电价等级的数量

        返回值:
            - sales_tariff(dict)
        """
        temp_dict = {
            "id": id,
            "salesTariffEntry": sales_tariff_entry
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if sales_tariff_description is not None:
            temp_dict["salesTariffDescription"] = sales_tariff_description
        if num_ePrice_levels is not None:
            temp_dict["numEPriceLevels"] = num_ePrice_levels
        return temp_dict

    @staticmethod
    def get_sales_tariff_entry_list(*sales_tariff_entry: dict) -> list:
        """
        生成 Sales Tariff Entry 列表

        参数:
            - sales_tariff_entry(dict): 电费套餐条目, 推荐使用 `get_sales_tariff_entry()` 传入, 参数个数范围为 [1, 1024]

        返回值:
            - sales_tariff_entry_list(list)
        """
        return [*sales_tariff_entry]

    @staticmethod
    def get_sales_tariff_entry(relative_time_interval: dict, custom_data: dict | None = None, ePrice_level: int | None = None, consumption_cost: list | None = None) -> dict:
        """
        生成 Sales Tariff Entry

        参数:
            - relative_time_interval(dict): 电费套餐条目时间区间, 推荐使用 `get_relative_time_interval()` 传入
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
            - ePrice_level(int): 电价等级,相对于NumEPriceLevels. EPriceLevel越小, 电费越低, 最小为0
            - consumption_cost(list): 电费套餐条目电费, 推荐使用 `get_consumption_cost_list()` 传入, 最少1条, 最多3条

        返回值:
            - sales_tariff_entry(dict)
        """
        temp_dict = {
            "relativeTimeInterval": relative_time_interval
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if ePrice_level is not None:
            temp_dict["ePriceLevel"] = ePrice_level
        if consumption_cost is not None:
            temp_dict["consumptionCost"] = consumption_cost
        return temp_dict

    @staticmethod
    def get_relative_time_interval(start: int, custom_data: dict | None = None, duration: dict | None = None) -> dict:
        """
        生成 Relative Time Interval

        参数:
            - start(int): 充电区间开始时间, 从现在算起的秒数
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
            - duration(int): 充电区间持续时间(单位: 秒)

        返回值:
            - relative_time_interval(dict)
        """
        temp_dict = {
            "start": start
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if duration is not None:
            temp_dict["duration"] = duration
        return temp_dict

    @staticmethod
    def get_consumption_cost_list(cost1: dict, cost2: dict | None = None, cost3: dict | None = None) -> list:
        """
        生成 consumptionCost 列表

        参数:
            - *cost(dict): 推荐使用 `get_consumption_cost()` 传入, 参数个数范围为 [1, 3]

        返回值:
            - temp(list)
        """
        temp = [cost1]
        if cost2 is not None:
            temp.append(cost2)
        if cost3 is not None:
            temp.append(cost3)
        return temp

    @staticmethod
    def get_consumption_cost(start_value: float, cost: list, custom_data: dict | None = None) -> dict:
        """
        生成 consumptionCost

        参数:
            - start_value(float): 区间消费起始点的最低消费等级
            - cost(list): 区间消费的成本, 最少1条, 最多3条, 推荐使用 `get_cost_list()` 传入
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
            - consumption_cost(dict)
        """
        temp_dict = {
            "startValue": start_value,
            "cost": cost
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_cost_list(cost1: dict, cost2: dict | None = None, cost3: dict | None = None) -> list:
        """
        生成 cost列表

        参数:
            - *cost(dict): 推荐使用 `get_cost()` 传入, 参数个数范围为 [1, 3]

        返回值:
            - temp(list)
        """
        temp = [cost1]
        if cost2 is not None:
            temp.append(cost2)
        if cost3 is not None:
            temp.append(cost3)
        return temp

    @staticmethod
    def get_cost(cost_kind: CostKindType | str, amount: int, custom_data: dict | None = None, amountMultiplier: int | None = None) -> dict:
        """
        生成 cost

        参数:
            - cost_kind(str): 成本类型,
                - `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`
                - 可以使用 `CostKindType` 枚举类, 例如:  `CostKindType.carbon_dioxide_emission`
            - amount(int): 每KWh的估计或实际成本
            - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
            - amountMultiplier(int): 成本乘数, 取值范围: [-3,3]

        返回值:
            - cost(dict)
        """
        temp_dict = {
            "costKind": cost_kind,
            "amount": amount
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if amountMultiplier is not None:
            temp_dict["amountMultiplier"] = amountMultiplier
        return temp_dict
