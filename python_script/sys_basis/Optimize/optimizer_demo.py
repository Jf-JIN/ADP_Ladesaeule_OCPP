import numpy as np
from scipy.optimize import linprog


class PeakShavingOptimizer:
    def __init__(self, demand, time_slots, max_power, max_grid_power):
        """
        初始化优化器
        :param demand: 每个充电桩的总需求 (list)
        :param time_slots: 时间段数 (int)
        :param max_power: 单个充电桩的最大功率限制 (float)
        :param max_grid_power: 电网允许的最大总功率 (float)
        """
        self.demand = demand
        self.time_slots = time_slots
        self.max_power = max_power
        self.max_grid_power = max_grid_power
        self.num_chargers = len(demand)

    def optimize(self):
        """
        优化错峰充电计划
        :return: 充电计划 (numpy array)
        """
        # 决策变量: 每个充电桩在每个时间段的充电功率
        num_variables = self.num_chargers * self.time_slots
        c = np.ones(num_variables)  # 目标函数, 尽量平滑功率, 简化为总功率最小化

        # 约束条件
        A_eq = []  # 满足每个充电桩的总需求
        b_eq = []
        for i, demand in enumerate(self.demand):
            row = [1 if j // self.time_slots == i else 0 for j in range(num_variables)]
            A_eq.append(row)
            b_eq.append(demand)

        A_ub = []  # 单桩功率限制和电网总功率限制
        b_ub = []
        # 单桩功率限制
        for i in range(num_variables):
            row = [0] * num_variables
            row[i] = 1
            A_ub.append(row)
            b_ub.append(self.max_power)

        # 电网总功率限制
        for t in range(self.time_slots):
            row = [1 if j % self.time_slots == t else 0 for j in range(num_variables)]
            A_ub.append(row)
            b_ub.append(self.max_grid_power)

        # 边界条件
        bounds = [(0, self.max_power) for _ in range(num_variables)]

        # 调用优化器
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if result.success:
            charging_schedule = result.x.reshape(self.num_chargers, self.time_slots)
            return charging_schedule
        else:
            raise ValueError("Optimization failed!")


# 示例使用
if __name__ == "__main__":
    demand = [20, 30, 40]  # 每个充电桩需要的总充电量
    time_slots = 10  # 时间段数量
    max_power = 10  # 单个充电桩的最大功率
    max_grid_power = 25  # 电网允许的最大总功率

    optimizer = PeakShavingOptimizer(demand, time_slots, max_power, max_grid_power)
    schedule = optimizer.optimize()
    print("充电计划: ")
    print(schedule)
