from ChargingNeedsRequest import *
from ChargingProfileRequest import *
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize
from sys_basis.Generator_Ocpp_Std.V2_0_1 import set_charging_profile_request


class Optimizer:
    """
    充电优化器
    
    参数: 
    - charging_needs(dict): 充电需求
    - eprices(list): 电价(间隔为15分钟)
    - his_usage(list): 历史的一天用电量(间隔为15分钟)
    - max_grid_power(int): 允许的最大电网功率
    - interval(int): 时间间隔(默认为15分钟)
    - mod(int): 模式(默认为0, 0表示动态调整, 1表示最小充电时间, 2表示最少电费花销)
    """

    def __init__(self, charging_needs: dict, eprices: list, his_usage: list, max_grid_power: int = 3000,
                 interval: int = 15, mod: int = 0):
        self._charging_needs = charging_needs
        self._energy_amount = self._charging_needs['acChargingParameters']['energyAmount']
        self._max_voltage = self._charging_needs['acChargingParameters']['evMaxVoltage']
        self._max_current = self._charging_needs['acChargingParameters']['evMaxCurrent']
        self._min_current = self._charging_needs['acChargingParameters']['evMinCurrent']
        self._departure_time = DataGene.str2time(self._charging_needs['departureTime'])
        self._eprices = eprices
        self._his_usage = his_usage
        self._max_grid_power = max_grid_power
        self._interval = interval
        self._mod = mod
        self._weight = self._get_weight()
        self._start_time = datetime.now() + timedelta(minutes=2)  # 2分钟计算和传输时间
        self._max_power = self._max_voltage * self._max_current
        self._min_power = self._max_voltage * self._min_current
        [self._time_split, self._eprices_split, self._max_power_split] = self._split_time(self._start_time,
            self._departure_time,
            self._eprices,
            self._his_usage,
            self._max_grid_power,
            self._max_power,
            self._min_power)
        self._num_split = len(self._time_split)
        print(self._num_split, "\n", self._time_split, "\n", self._eprices_split, "\n", self._max_power_split, "\n")
        self._charging_list = None
        self._over_time = 0
        self._cumulative_energy = []
        self._cost = []
        self._calculate_charging_list()

        # 初始化充电计划
        self._charging_schedule = []
        self._generate_charging_schedule()

    def get_charging_needs(self):
        return self._charging_needs

    def get_charging_schedule(self):
        return self._charging_schedule

    def _get_weight(self):
        """
        根据模式返回权重(默认为0, 0表示动态调整, 1表示最小充电时间, 2表示最少电费花销)
        """
        if self._mod == 0:
            return [0.5, 0.5]
        elif self._mod == 1:
            return [1, 0]
        elif self._mod == 2:
            return [0, 1]

    def _split_time(self, start_time: datetime, end_time: datetime, eprices: list, his_usage: list, max_grid_power: int, max_power: int, min_power: int) -> list:
        """
        将开始时间和结束时间按照15分钟间隔分割, 返回每段时间的持续时间、电价和可用功率. 

        参数: 
        - start_time(datetime): 开始时间
        - end_time(datetime): 结束时间
        - eprices(list): 电价列表
        - his_usage(list): 历史用电量列表
        - max_grid_power(int): 最大电网功率
        - max_power(int): 最大功率
        - min_power(int): 最小功率

        返回: 
        - list: 包含每段时间的持续时间、电价和可用功率的列表
        """
        result_time = []
        result_eprices = []
        max_power_list = []

        # 初始化第一个15分钟分割点
        time_15 = start_time + timedelta(minutes=(start_time.minute // 15 + 1) * 15 - start_time.minute)

        while start_time < end_time:
            # 确定当前时间段的结束时间
            segment_end = min(time_15, end_time)
            duration = (segment_end - start_time).seconds // 60
            result_time.append(duration)

            # 计算索引并获取电价
            start_index = (start_time.hour * 60 + start_time.minute) // 15
            result_eprices.append(eprices[start_index])

            # 计算可用功率
            available_power = max(min_power, max(0, max_grid_power - his_usage[start_index]))
            max_power_list.append(min(max_power, available_power))

            # 更新时间
            start_time = segment_end
            time_15 += timedelta(minutes=15)

        return [result_time, result_eprices, max_power_list]

    def _calculate_charging_list(self):
        """
        生成充电计划, 综合考虑以下因素: 
        1. 最短充电时间
        2. 最少电费花销
        3. 最大家庭充电负载限制
        """
        # T = self._num_split  # 总时间段
        E_target = self._energy_amount / 1000  # 目标充电量(kWh)
        # C = self._eprices_split  # 随机生成电价列表
        # w_over = self._weight[0]  # 充电时长权重
        # w_cost = self._weight[1]  # 充电成本权重
        # w_over = 1  # 充电时长权重
        # w_cost = 1  # 充电成本权重

        # 时间段长度 (小时)
        time_step = self._interval / 60

        # 动态功率范围
        P_min = [self._min_power / 1000] * self._num_split  # 每段的最小功率 (kW)
        P_max = [x / 1000 for x in self._max_power_split]  # 每段的最大功率 (kW)

        # 确保 P_min 不超过 P_max
        P_min = np.minimum(P_min, P_max)

        # 目标函数
        def cost_function(P):
            cumulative_energy = np.cumsum(P) * time_step
            over = np.argmax(cumulative_energy >= E_target) if np.any(cumulative_energy >= E_target) else self._num_split
            cost = np.sum(P * self._eprices_split * time_step)
            return self._weight[0] * over + self._weight[1] * cost

        # 约束条件
        constraints = {'type': 'ineq', 'fun': lambda P: np.sum(P) * time_step - E_target}

        # 动态边界
        bounds = [(P_min[i], P_max[i]) for i in range(self._num_split)]

        # 初始值
        P0 = np.full(self._num_split, np.mean(P_max))

        # 优化
        result = minimize(cost_function, P0, bounds=bounds, constraints=constraints)

        # 输出结果
        if result.success:
            self._charging_list = result.x
            cumulative_energy = np.cumsum(self._charging_list) * time_step
            self._over_time = np.argmax(cumulative_energy >= E_target) if np.any(cumulative_energy >= E_target) else self._num_split
            if self._over_time < self._num_split:
                self._charging_list[self._over_time + 1:] = P_min[self._over_time + 1:]
            self._cumulative_energy = np.cumsum(self._charging_list) * time_step
            self._cost = np.sum(self._charging_list * self._eprices_split * time_step)
            print("优化的充电功率列表: ", "\n", self._charging_list)
            print("累计充电:", "\n", self._cumulative_energy)
            print(f"充电完成时间段索引 (over): {self._over_time}")
            print(f"总成本 (cost): {self._cost:.2f}")
        else:
            print("优化失败")

    def _generate_charging_schedule(self):
        if self._charging_list is None:
            self._charging_schedule = None
        else:
            scpr = set_charging_profile_request()
            charging_schedule_period_list = []
            for i in range(self._num_split):
                start_period = sum(self._time_split[:i])
                charging_schedule_period_list.append(scpr.get_charging_schedule_period(start_period=start_period, limit=self._charging_list[i]))
            self._charging_schedule = scpr.get_charging_schedule(id=0, charging_rate_unit="w", charging_schedule_period=charging_schedule_period_list)


if __name__ == "__main__":
    from data_gene import *

    # charging_needs_request = {
    #     "evseId": 1,
    #     "chargingNeeds": {
    #         "requestedEnergyTransfer": EnergyTransferModeType.ac_three_phase,
    #         "acChargingParameters": {
    #             "energyAmount": 70000,
    #             "evMaxCurrent": 40,
    #             "evMinCurrent": 6,
    #             "evMaxVoltage": 400,
    #         },
    #         "departureTime": DataGene.time(10)
    #     }
    # }
    charging_needs = {
        "requestedEnergyTransfer": EnergyTransferModeType.ac_three_phase,
        "acChargingParameters": {
            "energyAmount": 70000,
            "evMaxCurrent": 32,
            "evMinCurrent": 6,
            "evMaxVoltage": 400,
        },
        "departureTime": DataGene.time2str(datetime(2025, 1, 3, 18, 18))
    }
    eprices = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    # print(eprices)
    his_usage = DataGene.gene_his_usage()
    # print(his_usage)
    # DataGene.plot_usage(his_usage)
    op_dp = Optimizer(charging_needs, eprices, his_usage, 16000)
    # print(op_dp.get_charging_needs())
    chargingschedule = op_dp.get_charging_schedule()
    print(chargingschedule)
