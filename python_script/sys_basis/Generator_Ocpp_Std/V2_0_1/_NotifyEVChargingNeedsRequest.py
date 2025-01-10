from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class GenNotifyEVChargingNeedsRequest(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        charging_needs: dict,
        evse_id: int,
        max_schedule_tuples: int | None = None,
        custom_data: dict | None = None
    ) -> call.NotifyEVChargingNeeds:
        """
        生成 NotifyEVChargingNeedsRequest

        - 参数: 
            - charging_needs(dict): 
                - 充电需求
                - 推荐使用 `get_charging_needs()` 传入
            - evse_id(int): 
                - EVSE的id, EvseId不可为0
            - max_schedule_tuples(int|None): 
                - 包含汽车每个计划支持的最大计划元组. 
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - call.NotifyEVChargingNeeds
        """
        return call.NotifyEVChargingNeeds(
            charging_needs=charging_needs,
            evse_id=evse_id,
            max_schedule_tuples=max_schedule_tuples,
            custom_data=custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.NotifyEVChargingNeeds:
        """
        加载字典数据, 将字典转换为数据类

        - 参数:
            - dict_data(dict): 字典数据

        - 返回值:
            - call.NotifyEVChargingNeeds
        """
        return call.NotifyEVChargingNeeds(
            charging_needs=dict_data['chargingNeeds'],
            evse_id=dict_data['evseId'],
            max_schedule_tuples=dict_data.get('maxScheduleTuples', None),
            custom_data=dict_data.get('customData', None)
        )

    @staticmethod
    def get_ac_charging_parameters(
        energy_amount: int,
        ev_min_current: int,
        ev_max_current: int,
        ev_max_voltage: int,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 ac charging parameters

        - 参数: 
            - energy_amount(int): 
                - 能量需求总数(单位: Wh). 这包括预处理所需的能量. 
            - ev_min_current(int): 
                - 电动汽车支持的每相最小电流(单位: A). 
            - ev_max_current(int): 
                - 电动汽车支持的每相最大电流(单位: A). 
            - ev_max_voltage(int): 
                - 电动汽车支持的每相最大电压(单位: V).
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入.

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'energyAmount': energy_amount,
            'evMinCurrent': ev_min_current,
            'evMaxCurrent': ev_max_current,
            'evMaxVoltage': ev_max_voltage
        }
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_dc_charging_parameters(
        ev_max_current: int,
        ev_max_voltage: int,
        energy_amount: int | None = None,
        ev_max_power: int | None = None,
        state_of_charge: int | None = None,
        ev_energy_capacity: int | None = None,
        fullsoc: int | None = None,
        bulksoc: int | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 dc charging parameters

        - 参数: 
            - ev_max_current(int): 
                - 电动汽车支持的最大电流(单位: A). 
            - ev_max_voltage(int): 
                - 电动汽车支持的最大电压(单位: V). 
            - energy_amount(int|None): 
                - 能量需求总数(单位: Wh), 包含预处理所需能量. 
            - ev_max_power(int|None): 
                - 电动汽车支持的最大功率(单位: W). 
            - state_of_charge(int|None): 
                - 电动汽车的当前充电状态(单位: %)
                - 长度范围: [0.0, 100.0]
            - ev_energy_capacity(int|None): 
                - 电动汽车的总能量容量(单位: Wh)
            - fullsoc(int|None): 
                - 电动汽车认为的充满电时的SoC百分比(单位: %).
                - 长度范围: [0.0, 100.0]
            - bulksoc(int|None): 
                - 电动汽车认为的快速充电过程结束时的SoC百分比(单位: %).
                - 长度范围: [0.0, 100.0]
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'evMaxCurrent': ev_max_current,
            'evMaxVoltage': ev_max_voltage
        }
        if energy_amount is not None:
            temp_dict['energyAmount'] = energy_amount
        if ev_max_power is not None:
            temp_dict['evMaxPower'] = ev_max_power
        if state_of_charge is not None:
            temp_dict['stateOfCharge'] = state_of_charge
        if ev_energy_capacity is not None:
            temp_dict['evEnergyCapacity'] = ev_energy_capacity
        if fullsoc is not None:
            temp_dict['fullSoC'] = fullsoc
        if bulksoc is not None:
            temp_dict['bulkSoC'] = bulksoc
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

    @staticmethod
    def get_charging_needs(
        requested_energy_transfer: str | EnergyTransferModeType,
        ac_charging_parameters: dict | None = None,
        dc_charging_parameters: dict | None = None,
        departure_time: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        生成 get_charging_needs

        - 参数: 
            - requested_energy_transfer(str): 
                - 能量传输模式. 
                - 枚举值: `DC`, `AC_single_phase`, `AC_two_phase`, `AC_three_phase`
                - 或使用枚举类(推荐)`EnergyTransferModeType`. e.g. `EnergyTransferModeType.dc`
            - ac_charging_parameters(dict|None): 
                - AC充电参数. 
                - 推荐使用 `get_ac_charging_parameters()` 传入
            - dc_charging_parameters(dict|None): 
                - DC充电参数  
                - 推荐使用 `get_dc_charging_parameters()` 传入
            - departure_time(str|None): 
                - 预计离开时间. 
                - 格式: date-time
            - custom_data(dict|None): 
                - 自定义数据.
                - 推荐使用 `get_custom_data()` 传入

        - 返回值:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'requestedEnergyTransfer': requested_energy_transfer
        }
        if ac_charging_parameters is not None:
            temp_dict['acChargingParameters'] = ac_charging_parameters
        if dc_charging_parameters is not None:
            temp_dict['dcChargingParameters'] = dc_charging_parameters
        if departure_time is not None:
            temp_dict['departureTime'] = departure_time
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict
