
from datetime import datetime, timedelta
from scipy.optimize import minimize
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from const.Const_Parameter import *
from tools.data_gene import DataGene
import numpy as np
_info = Log.OPT.info
_error = Log.OPT.error
_warning = Log.OPT.warning

class Optimizer:
    """
    充电优化器
    
    参数: 
        - charging_needs(dict): 充电需求
        - eprices(list): 电价(间隔为15分钟)
        - his_usage(list): 历史的一天用电量(间隔为15分钟)
        - max_grid_power(int): 允许的最大电网功率
        - interval(int): 时间间隔(默认为15分钟)
        - mode(int): 模式(默认为0, 0表示动态调整, 1表示最小充电时间, 2表示最少电费花销)

    方法:
        - get_charging_needs(): 获取充电需求
        - get_charging_schedule(): 获取充电计划
        - get_img_charging(): 获取充电图片
        - get_img_comparison(): 获取对比图片
        - Isopt(): 是否优化成功
    """

    def __init__(self, charging_needs: dict, eprices: list, his_usage: list, max_grid_power: int = 3000,
                 interval: int = 15, mode: int = 0):
        _info("--------------------Optimizer init--------------------")
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
        self._mode = mode
        self._change_rate = 0.05
        self._weight = self._get_weight()
        self._start_time = datetime.now() + timedelta(minutes=0)  # 2分钟计算和传输时间
        self._max_power = self._max_voltage * self._max_current
        self._min_power = self._max_voltage * self._min_current
        [self._time_split, self._eprices_split, self._max_power_split] = DataGene.split_time(
            self._start_time,
            self._departure_time,
            self._eprices,
            self._his_usage,
            self._max_grid_power,
            self._max_power,
            self._min_power,
            self._interval)
        self._num_split = len(self._time_split)
        self._charging_list = None
        self._over_time = 0
        self._cumulative_energy = []
        self._cost = []
        self._charging_schedule = []
        self._isopt = False
        if self._departure_time < datetime.now():
            _error("Departure time must be later than now")
        else:
            self._calculate_charging_list()
            self._generate_charging_schedule()

    def get_charging_needs(self):
        return self._charging_needs

    def get_charging_schedule(self):
        return self._charging_schedule

    def get_img_charging(self):
        if self._isopt:
            return DataGene.plot_charging_curve(
                self._start_time,
                self._time_split,
                self._charging_list
            )
        else:
            return None

    def get_img_comparison(self):
        if self._isopt:
            return DataGene.plot_usage_comparison(
                self._start_time,
                self._time_split,
                self._charging_list,
                self._his_usage,
                self._max_grid_power
            )
        else:
            return None

    def IsOpt(self):
        return self._isopt

    def _get_weight(self) -> list:
        """
        根据模式返回权重(默认为0, 0表示动态调整, 1表示最小充电时间, 2表示最少电费花销)
        """
        if self._mode == 0:
            return [0.5, 0.5]
        elif self._mode == 1:
            return [1, 0]
        elif self._mode == 2:
            return [0, 1]

    def _adjust_weights(self, time: float, cost: float) -> list:
        """
        动态调整权重
        """
        if time > cost:
            self._weight[0] += self._change_rate
            self._weight[1] -= self._change_rate
        else:
            self._weight[0] -= self._change_rate
            self._weight[1] += self._change_rate

        # 归一化
        total = sum(self._weight)
        return [w / total for w in self._weight]

    def _calculate_charging_list(self):
        """
        生成充电计划, 综合考虑以下因素:
        1. 最短充电时间
        2. 最少电费花销
        3. 最大家庭充电负载限制
        """
        E_target = self._energy_amount / 1000  # 目标充电量(Wh)

        # 时间段长度 (小时)
        time_step = self._interval / 60

        # 动态功率范围
        P_min = [self._min_power / 1000] * self._num_split  # 每段的最小功率 (W)
        P_max = [x / 1000 for x in self._max_power_split]  # 每段的最大功率 (W)

        # 确保 P_min 不超过 P_max
        P_min = np.minimum(P_min, P_max)

        # 目标函数
        def cost_function(P):
            cumulative_energy = np.cumsum(P) * time_step
            over = np.argmax(cumulative_energy >= E_target) if np.any(cumulative_energy >= E_target) else self._num_split
            cost_time = over * self._interval / 15
            cost = np.sum(P * self._eprices_split * time_step)
            if self._mode == 0:
                self._weight = self._adjust_weights(cost_time, cost)
            return self._weight[0] * cost_time + self._weight[1] * cost

        # 约束条件
        constraints = {'type': 'ineq', 'fun': lambda P: np.sum(P) * time_step - E_target}

        # 动态边界
        bounds = [(P_min[i], P_max[i]) for i in range(self._num_split)]

        # 初始值
        P0 = np.full(self._num_split, np.mean(P_max))
        # P0 = (P_min + P_max) / 2

        # 优化
        result = minimize(cost_function, P0, bounds=bounds, constraints=constraints)

        self._isopt = result.success
        # 输出结果
        if result.success:
            _info("--------------------Optimize Success----------------------")
            self._charging_list = result.x
            cumulative_energy = np.cumsum(self._charging_list) * time_step
            self._over_time = np.argmax(cumulative_energy >= E_target) if np.any(cumulative_energy >= E_target) else self._num_split
            if self._over_time < self._num_split:
                self._charging_list[self._over_time + 1:] = P_min[self._over_time + 1:]
            self._cumulative_energy = np.cumsum(self._charging_list) * time_step
            self._cost = np.sum(self._charging_list * self._eprices_split * time_step)
            _info("--------------------Optimization Result----------------------")
            _info("Optimized charging list (KW): ", "\n", self._charging_list)
            _info("Cumulative energy (KWh): ", "\n", self._cumulative_energy)
            _info(f"Charging completion time index: {self._over_time}")
            _info(f"Total cost: {self._cost:.2f}")
        else:
            _error("--------------------Optimization failed----------------------")

    def _generate_charging_schedule(self):
        """
        把列表转换成ocpp需要的格式
        """
        if self._charging_list is None:
            self._charging_schedule = None
        else:
            self._charging_list = [int(item * 1000) for item in self._charging_list]
            scpr = GenSetChargingProfileRequest()
            charging_schedule_period_list = []
            for i in range(self._num_split):
                start_period = int(sum(self._time_split[:i]) * 60)   # 缩短60倍用于测试，实际使用请删除
                charging_schedule_period_list.append(
                    scpr.get_charging_schedule_period(
                        start_period=start_period,
                        limit=self._charging_list[i]
                    )
                )
            self._charging_schedule = scpr.get_charging_schedule(
                id=1,
                charging_rate_unit="W",
                charging_schedule_period=charging_schedule_period_list,
                start_schedule=DataGene.time2str(self._start_time)
            )


if __name__ == "__main__":
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
    #         "departureTime": DataGene.time2str(datetime.now() + timedelta(hours=10))
    #     },
    #     "customData": {
    #         "vendorId": 123,
    #         "mode": 0
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
        "departureTime": DataGene.time2str(datetime.now() + timedelta(hours=10))
    }
    eprices = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    # print(eprices)
    his_usage = DataGene.gene_his_usage()
    # his_usage = DataGene.gene_his_usage_seed(3456)
    # print(his_usage)
    DataGene.plot_usage(his_usage)
    op_dp = Optimizer(charging_needs, eprices, his_usage, 16000, 30, 2)
    # print(op_dp.get_charging_needs())
    DataGene.plot_charging_curve(op_dp._start_time, op_dp._time_split, op_dp._charging_list)
    DataGene.plot_usage_comparison(op_dp._start_time, op_dp._time_split, op_dp._charging_list, his_usage, 16000)
