from dataclasses import dataclass, field
from ocpp.v201.enums import *


@dataclass
class Cost:
    cost_kind: CostKindType | str = ""
    amount: int = 0
    custom_data: dict | None = None
    amountMultiplier: int | None = None


@dataclass
class ConsumptionCost:
    start_value: float = 0.0
    cost: list[Cost] = field(default_factory=list)
    custom_data: dict | None = None


@dataclass
class RelativeTimeInterval:
    start: int = 0
    custom_data: dict | None = None
    duration: dict | None = None


@dataclass
class SalesTariffEntry:
    relative_time_interval: RelativeTimeInterval = field(default_factory=RelativeTimeInterval)
    custom_data: dict | None = None
    ePrice_level: int | None = None
    consumption_cost: list[ConsumptionCost] | None = None


@dataclass
class SalesTariff:
    id: int = 0
    sales_tariff_entry: list[SalesTariffEntry] = field(default_factory=list)
    custom_data: dict | None = None
    sales_tariff_description: str | None = None
    num_ePrice_levels: int | None = None


@dataclass
class ChargingSchedulePeriod:
    start_period: int = 0
    limit: float = 0.0
    custom_data: dict | None = None
    number_phases: int | None = None
    phase_to_use: int | None = None


@dataclass
class ChargingSchedule:
    id: int = 0
    charging_rate_unit: ChargingRateUnitType | str = ""
    charging_schedule_period: ChargingSchedulePeriod = field(default_factory=ChargingSchedulePeriod)
    custom_data: dict | None = None
    start_schedule: str | None = None
    duration: int | None = None
    min_charging_rate: float | None = None
    sales_tariff: SalesTariff | None = None


@dataclass
class ChargingScheduleRequest:
    time_base: str = ""
    evse_id: int = 0
    charging_schedule: ChargingSchedule = field(default_factory=ChargingSchedule)
    custom_data: dict | None = None
