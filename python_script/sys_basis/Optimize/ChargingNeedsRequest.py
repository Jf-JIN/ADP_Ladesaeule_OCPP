from dataclasses import dataclass, field
from ocpp.v201.enums import *


@dataclass
class AcChargingParameters:
    energy_amount: int = 0
    ev_min_current: int = 0
    ev_max_current: int = 0
    ev_max_voltage: int = 0
    custom_data: dict | None = None


@dataclass
class DcChargingParameters:
    ev_max_current: int = 0
    ev_max_voltage: int = 0
    custom_data: dict | None = None
    energy_amount: int | None = None
    ev_max_power: int | None = None
    state_of_charge: int | None = None
    ev_energy_capacity: int | None = None
    full_SoC: int | None = None
    bulk_SoC: int | None = None


@dataclass
class ChargingNeeds:
    requested_energy_transfer: EnergyTransferModeType | str = ""
    custom_data: dict | None = None
    ac_charging_parameters: AcChargingParameters | None = None
    dc_charging_parameters: DcChargingParameters | None = None
    departure_time: str | None = None


@dataclass
class ChargingNeedsRequest:
    charging_needs: ChargingNeeds = field(default_factory=ChargingNeeds)
    evse_id: int = 0
    max_schedule_tuples: int | None = None
    custom_data: dict | None = None
