import jsonschema
from ocpp.v201 import call
from ._Base import *
from const.Ocpp_Struct_Standard.V2_0_1.OCPP_Valid_Const import *
from ocpp.v201.enums import EnergyTransferModeType


class notify_ev_charging_needs_request(Base_OCPP_Struct_V2_0_1):
    @staticmethod
    def generate(evse_id: int, charging_needs: dict, custom_data: dict | None = None,
                 max_schedule_tuples: int | None = None) -> call.NotifyEVChargingNeeds:
        """
        生成 NotifyEVChargingNeedsRequest

        参数:
        - evse_id(int): EVSE的id，EvseId不可为0
        - charging_needs(dict): 充电需求，推荐使用 `get_charging_needs()` 传入
        - custom_data(dict): 自定义数据,推荐使用 `get_custom_data()` 传入
        - max_schedule_tuples(int): 车辆支持的每张计划表可容纳的最大元祖数

        返回值:
        - call.NotifyEVChargingNeeds
        """
        temp_dict = {
            "evseId": evse_id,
            "chargingNeeds": charging_needs
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if max_schedule_tuples is not None:
            temp_dict["maxScheduleTuples"] = max_schedule_tuples

        try:  # 官方数据类是下划线表示法, 官方检查文件用的是小驼峰, 注意区别! (-.-")
            jsonschema.validate(temp_dict, STD_v2_0_1.NotifyEVChargingNeedsRequest)
        except jsonschema.ValidationError as e:
            raise jsonschema.ValidationError(f"<notify_ev_charging_needs_request> 生成器 错误: {e.message}")

        return call.NotifyEVChargingNeeds(
            charging_needs=temp_dict["chargingNeeds"],
            evse_id=temp_dict["evseId"],
            max_schedule_tuples=temp_dict.get("maxScheduleTuples", None),
            custom_data=temp_dict.get("customData", None)
        )

    @staticmethod
    def get_charging_needs(requested_energy_transfer: EnergyTransferModeType | str,  custom_data: dict | None = None, ac_charging_parameters: dict | None = None,dc_charging_parameters: dict | None = None,departure_time: str | None = None) -> dict:
        """
        生成 Charging Needs

        参数:
        - requested_energy_transfer(str): 能量传输模式,直接使用EnergyTransferModeType枚举类或者自选: `DC`,`AC_single_phase`,`AC_two_phase`,`AC_three_phase`
        - custom_data(dict): 自定义数据,推荐使用 `get_custom_data()` 传入
        - ac_charging_parameters(dict): AC充电参数,推荐使用 `get_ac_charging_parameters()` 传入
        - dc_charging_parameters(dict): DC充电参数,推荐使用 `get_dc_charging_parameters()` 传入
        - departure_time(str): 预计离开时间,格式为`date-time`

        返回值:
        - charging_needs(dict)
        """
        temp_dict = {
            "requestedEnergyTransfer": requested_energy_transfer
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if ac_charging_parameters is not None:
            temp_dict["acChargingParameters"] = ac_charging_parameters
        if dc_charging_parameters is not None:
            temp_dict["dcChargingParameters"] = dc_charging_parameters
        if departure_time is not None:
            temp_dict["departureTime"] = departure_time
        return temp_dict


    @staticmethod
    def get_ac_charging_parameters(energy_amount: int, ev_min_current: int, ev_max_current: int, ev_max_voltage: int, custom_data: dict | None = None) -> dict:
        """
        生成 AC Charging Parameters

        参数:
        - energy_amount(int): 能量需求总数(单位：Wh)
        - ev_min_current(int): 电动汽车支持的每相最小电流(单位：A)
        - ev_max_current(int): 电动汽车支持的每相最大电流(单位：A)
        - ev_max_voltage(int): 电动汽车支持的每相最大电压(单位：V)
        - custom_data(dict): 自定义数据,推荐使用 `get_custom_data()` 传入

        返回值:
        - acChargingParameters(dict)
        """
        temp_dict = {
            "energyAmount": energy_amount,
            "evMinCurrent": ev_min_current,
            "evMaxCurrent": ev_max_current,
            "evMaxVoltage": ev_max_voltage
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        return temp_dict

    @staticmethod
    def get_dc_charging_parameters(ev_max_current: int, ev_max_voltage: int, custom_data: dict | None = None, energy_amount: int | None = None, ev_max_power: int | None = None, state_of_charge: int | None = None, ev_energy_capacity: int | None = None, full_SoC: int | None = None, bulk_SoC: int | None = None) -> dict:
        """
        生成 DC Charging Parameters

        参数:
        - ev_max_current(int): 电动汽车支持的最大电流(单位：A)
        - ev_max_voltage(int): 电动汽车支持的最大电压(单位：V)
        - custom_data(dict): 自定义数据,推荐使用 `get_custom_data()` 传入
        - energy_amount(int): 能量需求总数(单位：Wh)，包含预处理所需能量
        - ev_max_power(int): 电动汽车支持的最大功率(单位：W)
        - state_of_charge(int): 电动汽车的当前充电状态(单位：%)，取值范围：[0,100]
        - ev_energy_capacity(int): 电动汽车的总能量容量(单位：Wh)
        - full_SoC(int): 电动汽车认为的充满电时的SoC百分比(单位：%)，取值范围：[0,100]
        - bulk_SoC(int): 电动汽车认为的快速充电过程结束时的SoC百分比(单位：%)，取值范围：[0,100]

        返回值:
        - dcChargingParameters(dict)
        """
        temp_dict = {
            "evMaxCurrent": ev_max_current,
            "evMaxVoltage": ev_max_voltage
        }
        if custom_data is not None:
            temp_dict["customData"] = custom_data
        if energy_amount is not None:
            temp_dict["energyAmount"] = energy_amount
        if ev_max_power is not None:
            temp_dict["evMaxPower"] = ev_max_power
        if state_of_charge is not None:
            temp_dict["stateOfCharge"] = state_of_charge
        if ev_energy_capacity is not None:
            temp_dict["evEnergyCapacity"] = ev_energy_capacity
        if full_SoC is not None:
            temp_dict["fullSoC"] = full_SoC
        if bulk_SoC is not None:
            temp_dict["bulkSoC"] = bulk_SoC
        return temp_dict
