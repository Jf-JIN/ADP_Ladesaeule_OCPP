from sys_basis.XSignal import XSignal
from _EVSE_manager import EVSEManager
from _Shelly_manager import ShellyManager


class GPIOManager:
    """
    参数:
    - RCD: bool, 是否安装RCD
    - new_charge: bool, 是否是新的一次充电
    信号:
    -   __signal_GPIO_min_current: 允许最小电流
    -   __signal_GPIO_actual_current: EVSE实际电流
    -   __signal_GPIO_EVSE_failure: EVSE故障
    -   __signal_GPIO_vehicle_state: 车辆状态
    -   __signal_GPIO_Shelly_error: Shelly故障
    -   __signal_GPIO_Shelly_data: Shelly数据,格式如下,列表的0,1,2位代表第1,2,3个电流钳数据
        {
            'power': [0, 10, 20],
            'pf': [0, 0.95, 0.9],
            'current': [0, 5, 10],
            'voltage': [0, 220, 215],
            'is_valid': [True, True, True],
            'total': [0, 100, 200],
            'total_returned': [0, 5, 10]
        }
    方法:
    - set_current: 设置EVSE输出电流
    """
    def __init__(self,RCD: bool,new_charge: bool):
        self.evse = EVSEManager(RCD)
        self.shelly = ShellyManager(new_charge)

        self.__signal_GPIO_min_current = XSignal()
        self.__signal_GPIO_actual_current = XSignal()
        self.__signal_GPIO_EVSE_failure = XSignal()
        self.__signal_GPIO_vehicle_state = XSignal()
        self.__signal_GPIO_Shelly_error = XSignal()
        self.__signal_GPIO_Shelly_data = XSignal()

        self.evse.signal_EVSE_min_current.connect(self.signal_GPIO_min_current.emit)
        self.evse.signal_EVSE_actual_current.connect(self.signal_GPIO_actual_current.emit)
        self.evse.signal_EVSE_failure.connect(self.signal_GPIO_EVSE_failure.emit)
        self.evse.signal_vehicle_state.connect(self.signal_GPIO_vehicle_state.emit)
        self.shelly.signal_Shelly_error.connect(self.signal_GPIO_Shelly_error.emit)
        self.shelly.signal_Shelly_data.connect(self.signal_GPIO_Shelly_data.emit)


    @property
    def signal_GPIO_min_current(self):
        return self.__signal_GPIO_min_current

    @property
    def signal_GPIO_actual_current(self):
        return self.__signal_GPIO_actual_current

    @property
    def signal_GPIO_EVSE_failure(self):
        return self.__signal_GPIO_EVSE_failure

    @property
    def signal_GPIO_vehicle_state(self):
        return self.__signal_GPIO_vehicle_state

    @property
    def signal_GPIO_Shelly_error(self):
        return self.__signal_GPIO_Shelly_error

    @property
    def signal_GPIO_Shelly_data(self):
        return self.__signal_GPIO_Shelly_data


    def set_current(self,current):
        self.evse.set_current(current)

