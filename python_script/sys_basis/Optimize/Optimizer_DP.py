

class OptimizerDP:
    """
    充电优化器（使用动态规划）
    
    参数：
    - charging_needs_request(dict): 充电需求请求字典
        - evse_id(int): EVSE的id, EvseId不可为0
        - charging_needs(dict): 充电需求, 推荐使用 `get_charging_needs()` 传入
        - custom_data(dict): 自定义数据, 推荐使用 `get_custom_data()` 传入
        - max_schedule_tuples(int): 车辆支持的每张计划表可容纳的最大元祖数 
    """
    def __init__(self, charging_needs_request):
        self.evse_id = charging_needs_request['evseId']
        self.charging_needs = charging_needs_request['chargingNeeds']
        self.custom_data = charging_needs_request.get("customData", None)
        self.max_schedule_tuples = charging_needs_request.get("maxScheduleTuples", None)

        # 初始化充电计划
        self._charging_schedule = []

    def get_charging_schedule(self):
        """
        获取优化后的充电计划。

        返回：
        - list: 充电计划列表，每个计划包含时间段和充电功率。
        """
        if not self._charging_schedule:
            self._generate_charging_schedule()
        return self._charging_schedule

    def _generate_charging_schedule(self):
        """
        使用动态规划算法生成充电计划。
        """
        charging_needs = self.charging_needs
