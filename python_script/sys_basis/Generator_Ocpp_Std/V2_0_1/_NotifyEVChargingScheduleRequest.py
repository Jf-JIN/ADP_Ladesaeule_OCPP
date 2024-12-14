
from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_ev_charging_schedule_request(Base_OCPP_Struct_V2_0_1):
    @staticmethod
    def generate(time_base: str, evse_id: int, charging_schedule: dict, custom_data: dict | None = None, **kwargs) -> call.NotifyEVChargingSchedule:
        """
        生成 NotifyEVChargingScheduleRequest

        参数:
        - time_base(str): 充电配置文件中的时间基准
        - evse_id(int): 充电计划表中使用中的EvseId. EvseId 必须 > 0. 
        - charging_schedule(dict): 充电计划表,  推荐使用 `get_charging_schedule()` 传入
        - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入

        返回值:
        - call_result.NotifyEVChargingSchedule
        """

        return call.NotifyEVChargingSchedule(
            time_base=time_base or kwargs.get('time_base', None),
            evse_id=evse_id or kwargs.get('evse_id', None),
            charging_schedule=charging_schedule or kwargs.get('charging_schedule', None),
            custom_data=custom_data or kwargs.get('custom_data', None)
        )

    @staticmethod
    def get_charging_schedule(id: int, charging_rate_unit: ChargingRateUnitType | str, charging_schedule_period: dict, custom_data: dict | None = None, start_schedule: str | None = None, duration: int | None = None, min_charging_rate: float | None = None, sales_tariff: dict | None = None) -> dict:
        """
        生成 Charging Schedule

        参数:
        - id(int): 充电计划表的标识
        - charging_rate_unit(str): 充电速率单位, 直接使用ChargingRateUnitType枚举类或者自选: `W`, `A`
        - charging_schedule_period(dict): 充电计划表周期, 推荐使用 `get_charging_schedule_period()` 传入
        - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
        - start_schedule(str): 充电计划表的绝对起始时间, 如果缺失, 则等同于充电开始时间
        - duration(int): 充电计划表持续时间(单位: 秒), 如果缺失, 最后一个周期将无限循环, 直到交易结束
        - min_charging_rate(float): 电动汽车支持的最小充电速率
        - sales_tariff(dict): 电费套餐, 推荐使用 `get_sales_tariff()` 传入

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
    def get_charging_schedule_period(start_period: int, limit: float, custom_data: dict | None = None, number_phases: int | None = None, phase_to_use: int | None = None) -> dict:
        """
        生成 Charging Schedule Period

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
        生成 Sales Tariff Entry List

        参数:
        - sales_tariff_entry(dict): 电费套餐条目, 推荐使用 `get_sales_tariff_entry()` 传入

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
    def get_consumption_cost_list(*consumption_cost: dict) -> list:
        """
        生成 consumptionCost列表

        参数:
        - *consumption_cost(dict): 推荐使用 `get_consumption_cost()` 传入

        返回值:
        - consumption_cost(list)
        """
        return [*consumption_cost]

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
    def get_cost_list(*cost: dict) -> list:
        """
        生成 cost列表

        参数:
        - *cost(dict): 推荐使用 `get_cost()` 传入

        返回值:
        - cost(list)
        """
        return [*cost]

    @staticmethod
    def get_cost(cost_kind: CostKindType | str, amount: int, custom_data: dict | None = None, amountMultiplier: int | None = None) -> dict:
        """
        生成 cost

        参数:
        - cost_kind(str): 成本类型,直接使用CostKindType枚举类或者自选: `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`
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
