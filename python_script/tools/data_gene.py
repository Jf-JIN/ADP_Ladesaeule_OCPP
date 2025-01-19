from datetime import datetime, timedelta
import numpy as np
import pytz
import matplotlib.pyplot as plt
import io
import base64
from const.Const_Parameter import *
_info = Log.OPT.info
_error = Log.OPT.error
_warning = Log.OPT.warning

class DataGene:
    """
    数据生成类, 用于生成电价, 时间, 家庭用电数据等数据

    静态方法: 
        - `gene_eprices`: 生成电价列表(区分日间, 夜间电价)
        - `time2str`: 生成指定字符串格式的柏林时间
        - `str2time`: 将字符串格式时间(柏林时间)转换为 datetime 对象
        - `gene_his_usage`: 生成一天家庭的用电数据, 每隔15分钟一个数据点, 单位为Wh
        - `plot_usage`: 绘制用电数据图
        - `plot_charging_schedule`: 根据优化前和优化后的用电记录绘制家庭用电曲线图
        - `split_time`: 将开始时间和结束时间按照15分钟间隔分割, 返回每段时间的持续时间、电价和可用功率.
    """

    @staticmethod
    def gene_eprices(price1: float, price2: float = None, time1: int = None, time2: int = None) -> list:
        """
        生成电价列表(区分日间, 夜间电价)

        参数: 
            - price1(float): 日间电价
            - price2(float): 夜间电价(可选, 如果没有提供则默认所有时间段都使用日间电价)
            - time1(int): 夜间电价结束时间(小时, 可选)
            - time2(int): 夜间电价开始时间(小时, 可选)

        返回: 
            - price_schedule(list): 电价列表(每隔15分钟)
        """

        # 默认夜间电价参数
        if price2 is None or time1 is None or time2 is None:
            price2, time1, time2 = price1, 0, 0

        # 每隔15分钟计算电价
        price_schedule = [
            price1 if time1 <= hour < time2 else price2
            for hour in range(24)  # 每小时
            for _ in range(4)  # 每小时有4个15分钟段
        ]
        return price_schedule

    @staticmethod
    def time2str(time: datetime) -> str:
        """
        生成指定字符串格式的柏林时间. 

        参数: 
            - time(datetime): 需要转换的时间对象

        返回: 
            - str: 格式化后的柏林时间字符串(ISO 8601 格式, 德国时区)
        """
        return time.astimezone(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def str2time(time_str: str) -> datetime:
        """
        将字符串格式时间(柏林时间)转换为 datetime 对象

        参数: 
            - time_str(str): 格式化的时间字符串('%Y-%m-%dT%H:%M:%SZ')

        返回: 
            - datetime: 转换后的 datetime 对象(无时区信息)
        """
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def gene_his_usage_seed(fixed_user_id: int = None) -> list[int]:
        """
        生成一天家庭的用电数据, 每隔15分钟一个数据点, 单位为W.
        如果传入固定用户ID, 则生成固定的用电数据. 

        参数:
            - fixed_user_id (int): 固定的用户ID, 用于生成固定数据. 为None时, 数据是随机的. 

        返回:
            - list[int]: 一天的用电数据
        """

        def generate_usage(hour: int, seed: int) -> int:
            """根据小时和种子生成用电量(单位: Wh). """
            np.random.seed(seed)
            if 6 <= hour < 18:  # 白天
                usage = np.random.normal(5000, 500)
                if 7 <= hour < 9:  # 早餐时间
                    usage += np.random.normal(2000, 300)
                elif 12 <= hour < 14:  # 午餐时间
                    usage += np.random.normal(1600, 200)
            else:  # 夜间
                usage = np.random.normal(1000, 300)
                if 19 <= hour < 22:  # 晚上电视和照明
                    usage += np.random.normal(2400, 500)
                if 20 <= hour < 22:  # 晚上洗澡
                    usage += np.random.normal(3000, 400)
                elif 22 <= hour < 23:  # 晚上用电渐低
                    usage += np.random.normal(1200, 300)
            return max(0, int(usage))  # 确保用电量非负

        # 如果有固定的用户ID, 使用该ID生成固定的种子
        seed = fixed_user_id if fixed_user_id is not None else np.random.randint(0, 100000)

        # 每天有96个15分钟数据点
        return [generate_usage(i // 4, seed) for i in range(96)]

    @staticmethod
    def gene_his_usage() -> list[int]:
        """
        生成一天家庭的用电数据, 每隔15分钟一个数据点, 单位为W.

        返回:
            - list[int]: 一天的用电数据
        """

        def generate_usage(hour: int) -> int:
            """根据小时生成用电量(单位: W). """
            if 6 <= hour < 18:  # 白天
                usage = np.random.normal(5000, 500)
                if 7 <= hour < 9:  # 早餐时间
                    usage += np.random.normal(2000, 300)
                elif 12 <= hour < 14:  # 午餐时间
                    usage += np.random.normal(1600, 200)
            else:  # 夜间
                usage = np.random.normal(1000, 300)
                if 19 <= hour < 22:  # 晚上电视和照明
                    usage += np.random.normal(2400, 500)
                if 20 <= hour < 22:  # 晚上洗澡
                    usage += np.random.normal(3000, 400)
                elif 22 <= hour < 23:  # 晚上用电渐低
                    usage += np.random.normal(1200, 300)
            return max(0, int(usage))  # 确保用电量非负

        # 每天有96个15分钟数据点
        return [generate_usage(i // 4) for i in range(96)]

    @staticmethod
    def plot_usage(usage_record: list):
        """
        根据用电记录绘制家庭用电曲线图

        参数: 
            - usage_record: 一个包含每15分钟用电数据的列表(单位: W)
        """
        # 确定时间段, 24小时内, 每小时4个数据点, 总共96个数据点
        time_slots = np.arange(len(usage_record))  # 生成0到95的时间段(每15分钟一个数据点)

        # 每小时的标签(显示小时数)
        hours_labels = np.arange(0, 24, 2)  # 每2小时一个标签
        time_labels = [f"{hour}:00" for hour in hours_labels]  # 创建小时标签

        # 绘制用电量图
        plt.figure(figsize=(10, 6))
        plt.plot(time_slots, usage_record, label='Electricity Usage (Wh)', color='b')

        # 设置坐标轴和标题
        plt.xlabel('Time Slots (15 minutes)')
        plt.ylabel('Electricity Usage (Wh)')
        plt.title('Electricity Usage Throughout the Day (15-Minute Intervals)')

        # 设置X轴刻度为每小时, 并调整显示
        plt.xticks(np.arange(0, 96, 8), labels=time_labels)  # 每8个点为2个小时
        plt.grid(True)
        plt.tight_layout()  # 自适应调整布局, 避免标签重叠
        plt.show()

    @staticmethod
    def plot_charging_curve(start_time, time_split, charging_list) -> str:
        """
        绘制充电曲线图

        参数:
            - start_time: 充电开始时间
            - time_split: 每次充电的持续时间(单位: 分钟)
            - charging_list: 每次充电的功率(单位: W)

        返回:
            - str: 充电曲线图的base64编码字符串
        """
        times = [start_time]
        cumulative_energy = [0]
        for duration, power in zip(time_split, charging_list):
            cumulative_energy.append(cumulative_energy[-1] + power * duration / 60)
            times.append(times[-1] + timedelta(minutes=duration))

        plt.figure(figsize=(12, 6))
        plt.step(times, cumulative_energy, where='post')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Energy (Wh)')
        plt.title('Cumulative Charging Energy Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        # plt.show()
        # save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        base64_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return base64_image

    @staticmethod
    def plot_usage_comparison(start_time, time_split, charging_list, his_usage, max_grid_power) -> str:
        """
        绘制用电量对比图

        参数:
            - start_time: 充电开始时间
            - time_split: 每次充电的持续时间(单位: 分钟)
            - charging_list: 每次充电的功率(单位: W)
            - his_usage: 历史用电记录(单位: W)
            - max_grid_power: 最大电网功率(单位: W)

        返回:
            - str: 用电量对比图的base64编码字符串
        """
        times = [start_time]
        for duration, power in zip(time_split, charging_list):
            times.append(times[-1] + timedelta(minutes=duration))

        # Calculate matching historical usage for each time point
        updated_usage = []
        original_usage = []
        for i, (start, power) in enumerate(zip(times[:-1], charging_list)):
            matching_index = int((start - start_time.replace(hour=0, minute=0)).total_seconds() // 900)
            matching_usage = his_usage[matching_index % len(his_usage)]
            original_usage.append(matching_usage)
            updated_usage.append(matching_usage + power)

        plt.figure(figsize=(12, 6))
        plt.plot(times[:-1], original_usage, label='Historical Usage', linestyle='--')
        plt.plot(times[:-1], updated_usage, label='Updated Usage', linestyle='-')
        plt.axhline(y=max_grid_power, color='r', linestyle=':', label='Max Grid Power')
        plt.xlabel('Time')
        plt.ylabel('Power (W)')
        plt.title('Power Usage Comparison')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        # plt.show()
        # save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        base64_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return base64_image

    @staticmethod
    def split_time(
            start_time: datetime,
            end_time: datetime,
            eprices: list,
            his_usage: list,
            max_grid_power: int,
            max_power: int,
            min_power: int,
            interval: int = 15
    ) -> list:
        """
        将开始时间和结束时间按照给定的分钟间隔分割, 返回每段时间的持续时间、电价和可用功率.

        参数:
            - start_time(datetime): 开始时间
            - end_time(datetime): 结束时间
            - eprices(list): 电价列表（每15分钟一个数）
            - his_usage(list): 历史用电量列表（每15分钟一个数）
            - max_grid_power(int): 最大电网功率
            - max_power(int): 最大功率
            - min_power(int): 最小功率
            - interval(int): 分割间隔（可选15, 30, 60, 120分钟）

        返回:
            - list: 包含每段时间的持续时间、电价和可用功率的列表
        """
        # if interval not in [15, 30, 60, 120]:
        #     _error("Interval must be one of [15, 30, 60, 120]")

        if interval not in [15, 30, 60, 120]:
            _error("Interval must be one of [15, 30, 60, 120]")

        result_time = []
        result_eprices = []
        max_power_list = []

        # 初始化第一个分割点
        time_next = start_time + timedelta(minutes=interval - start_time.minute % interval)

        while start_time < end_time:
            # 确定当前时间段的结束时间
            segment_end = min(time_next, end_time)
            duration = (segment_end - start_time).seconds // 60
            result_time.append(duration)

            # 计算索引范围
            start_index = (start_time.hour * 60 + start_time.minute) // 15
            end_index = (segment_end.hour * 60 + segment_end.minute) // 15
            # _info(f"start_index: {start_index}, end_index: {end_index}")

            # 避免除以零的错误
            if end_index > start_index:
                avg_price = sum(eprices[start_index:end_index]) / (end_index - start_index)
                avg_usage = sum(his_usage[start_index:end_index]) / (end_index - start_index)
            else:
                avg_price = eprices[start_index]
                avg_usage = his_usage[start_index]

            result_eprices.append(avg_price)

            # 计算可用功率
            available_power = max(min_power, max(0, max_grid_power - avg_usage))
            max_power_list.append(min(max_power, available_power))

            # 更新时间
            start_time = segment_end
            time_next += timedelta(minutes=interval)

        return [result_time, result_eprices, max_power_list]


if __name__ == "__main__":
    eprices = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    his_usage = DataGene.gene_his_usage()
    # DataGene.plot_usage(eprices)
    # DataGene.plot_usage(his_usage)
    # print(DataGene.time2str())
    # print(datetime.now())
    # print(DataGene.str2time('2024-07-25T10:00:00Z'))
    start = DataGene.str2time('2024-12-29T21:12:00Z')
    [time_split, eprices_split, max_power_split] = DataGene.split_time(start, start+timedelta(hours=8), eprices, his_usage, 16000, 12800, 2400, 60)
    print(time_split, eprices_split, max_power_split)
