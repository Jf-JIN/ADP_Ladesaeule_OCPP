from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class notify_ev_charging_schedule_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        time_base: str,
        charging_schedule: dict,
        evse_id: int,
        custom_data: dict | None = None
    ) -> call.NotifyEVChargingSchedule:
        """
        生成 NotifyEVChargingScheduleRequest

        - 参数: 
            - time_base(str): 
                - 充电配置文件中的时间基准. 
                - 格式: date-time
            - charging_schedule(dict): 
                - 充电计划表, Charging_Schedule 充电时间表结构定义了充电周期列表, 用于: GetCompositeSchedule.conf 和 ChargingProfile. 
                - 推荐使用 `get_charging_schedule()` 传入
            - evse_id(int): 
                - 充电计划表中使用中的EvseId. EvseId 必须 > 0. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.NotifyEVChargingSchedule
        """
        return call.NotifyEVChargingSchedule(
            time_base=time_base,
            charging_schedule=charging_schedule,
            evse_id=evse_id,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEVChargingSchedule:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.NotifyEVChargingSchedule
        """
        return call.NotifyEVChargingSchedule(
            time_base=dict_data['timeBase'],
            charging_schedule=dict_data['chargingSchedule'],
            evse_id=dict_data['evseId'],
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_charging_schedule_period(
        start_period: int,
        limit: int | float,
        number_phases: int | None = None,
        phase_to_use: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 charging schedule period

        - 参数: 
            - start_period(int): 
                - 充电计划表的周期开始时间, 也代表了上一周期的结束时间(单位: 秒)
            - limit(int|float): 
                - 计划期间的充电速率限制. 以适用的充电速率单位(例如安培 (A) 或瓦特 (W))测量计划期间的充电速率限制. 最多接受一位小数(例如 8.1). 
            - number_phases(int|None): 
                - 充电可使用的相数. 如果需要多个阶段, 则将假定 numberPhases=3, 除非给出另一个数字. 
            - phase_to_use(int|None): 
                - 值: 1..3, 仅在numberPhases=1并且EVSE能够切换连接到EV的相位, 即 ACPhaseSwitchingSupported已定义且为true的情况下使用. 除非上述两个条件都成立, 否则不允许这样做. 如果两个条件都为真, 并且省略phaseToUse, 则充电站/EVSE将自行做出选择. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'startPeriod': start_period,
            'limit': limit
        }
        if number_phases is not None:
            temp_dict['numberPhases'] = number_phases
        if phase_to_use is not None:
            temp_dict['phaseToUse'] = phase_to_use
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_relative_time_interval(
        start: int,
        duration: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 relative time interval

        - 参数: 
            - start(int): 
                - 充电区间开始时间, 从现在算起的秒数 
            - duration(int|None): 
                - 充电区间持续时间(单位: 秒)
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'start': start
        }
        if duration is not None:
            temp_dict['duration'] = duration
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_cost(
        cost_kind: str | CostKindType,
        amount: int,
        amount_multiplier: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 cost

        - 参数: 
            - cost_kind(str): 
                - 成本类型. 消息元素金额中引用的成本种类 
                - 枚举值: `CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`
                - 或使用枚举类(推荐)`CostKindType`. e.g. `CostKindType.carbon_dioxide_emission`
            - amount(int): 
                - 每 `KWh` 的估计或实际成本 
            - amount_multiplier(int|None): 
                - 成本乘数. 整数值: -3..3,  amountMultiplier 定义以 10 为底的指数 (dec). 最终值由以下公式确定:  amount *10 ^ amountMultiplier
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'costKind': cost_kind,
            'amount': amount
        }
        if amount_multiplier is not None:
            temp_dict['amountMultiplier'] = amount_multiplier
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_consumption_cost(
        start_value: int | float,
        cost: list,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 consumption cost

        - 参数: 
            - start_value(int|float): 
                - 区间消费起始点的最低消费等级, 定义此消耗块起点的最低消耗级别. 块间​​隔延伸到下一个间隔的开始. 
            - cost(list): 
                - 区间消费的成本
                - 长度范围: [1, 3]
                - 推荐使用 `get_cost()` 传入列表元素 或 自行创建列表.
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'startValue': start_value,
            'cost': cost
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_sales_tariff_entry(
        relative_time_interval: dict,
        e_price_level: int | None = None,
        consumption_cost: list | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 sales tariff entry

        - 参数: 
            - relative_time_interval(dict): 
                - 电费套餐条目时间区间
                - 推荐使用 `get_relative_time_interval()` 传入
            - e_price_level(int|None): 
                - 电价等级,相对于NumEPriceLevels. EPriceLevel越小, 电费越低, 最小为0. Unsigned_ Integer 定义此 SalesTariffEntry 的价格水平(参考 NumEPriceLevels). EPriceLevel 的较小值表示较便宜的 TariffEntry. EPriceLevel 的较大值表示更昂贵的 TariffEntry. 
            - consumption_cost(list|None): 
                - 电费套餐条目电费
                - 长度范围: [1, 3]
                - 推荐使用 `get_consumption_cost()` 传入列表元素 或 自行创建列表.
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'relativeTimeInterval': relative_time_interval
        }
        if e_price_level is not None:
            temp_dict['ePriceLevel'] = e_price_level
        if consumption_cost is not None:
            temp_dict['consumptionCost'] = consumption_cost
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_sales_tariff(
        id: int,
        sales_tariff_entry: list,
        sales_tariff_description: str | None = None,
        num_eprice_levels: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 sales tariff

        - 参数: 
            - id(int): 
                - 电费套餐的标识, 用于标识一种销售费率. SAID 在整个充电会话中仍然是一个时间表的唯一标识符. 
            - sales_tariff_entry(list): 
                - Sales_ Tariff_ Entry 
                - 长度范围: [1, 1024]
                - 推荐使用 `get_sales_tariff_entry()` 传入列表元素 或 自行创建列表.
            - sales_tariff_description(str|None): 
                - 电费套餐的描述. 人类可读的销售关税标题/简短描述, 例如用于 HMI 显示目的
                - 长度范围: [1, 32]
            - num_eprice_levels(int|None): 
                - 电费套餐条目中涉及的电价等级的数量, 定义所有提供的 SalesTariff 元素中使用的不同价格水平的总数. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id,
            'salesTariffEntry': sales_tariff_entry
        }
        if sales_tariff_description is not None:
            temp_dict['salesTariffDescription'] = sales_tariff_description
        if num_eprice_levels is not None:
            temp_dict['numEPriceLevels'] = num_eprice_levels
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_schedule(
        id: int,
        charging_rate_unit: str | ChargingRateUnitType,
        charging_schedule_period: list,
        start_schedule: str | None = None,
        duration: int | None = None,
        min_charging_rate: int | float | None = None,
        sales_tariff: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 charging schedule

        - 参数: 
            - id(int): 
                - 充电计划表的标识. 
            - charging_rate_unit(str): 
                - 充电速率单位. 
                - 枚举值: `W`, `A`
                - 或使用枚举类(推荐)`ChargingRateUnitType`. e.g. `ChargingRateUnitType.w`
            - charging_schedule_period(list): 
                - 充电计划表周期. 其定义了充电时间表中的时间段. 
                - 长度范围: [1, 1024]
                - 推荐使用 `get_charging_schedule_period()` 传入列表元素 或 自行创建列表.
            - start_schedule(str|None): 
                - 充电计划表的绝对起始时间, 如果缺失, 则等同于充电开始时间. 
                - 格式: date-time
            - duration(int|None): 
                - 充电计划表持续时间(单位: 秒), 如果缺失, 最后一个周期将无限循环, 直到交易结束, 或 chargingProfilePurpose = TxProfile . 
            - min_charging_rate(int|float|None): 
                - 电动汽车支持的最小充电速率. 数字 EV 支持的最低充电率. 测量单位由chargingRateUnit 定义. 该参数旨在供本地智能充电算法使用, 以在充电过程在较低充电速率下效率低下的情况下优化功率分配. 最多接受一位小数(例如 8.1) 
            - sales_tariff(dict|None): 
                - 电费套餐. 注意: 此数据类型基于 <<ref-ISOIEC15118-2,ISO 15118-2>> 中的数据类型. 
                - 推荐使用 `get_sales_tariff()` 传入
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'id': id,
            'chargingRateUnit': charging_rate_unit,
            'chargingSchedulePeriod': charging_schedule_period
        }
        if start_schedule is not None:
            temp_dict['startSchedule'] = start_schedule
        if duration is not None:
            temp_dict['duration'] = duration
        if min_charging_rate is not None:
            temp_dict['minChargingRate'] = min_charging_rate
        if sales_tariff is not None:
            temp_dict['salesTariff'] = sales_tariff
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
