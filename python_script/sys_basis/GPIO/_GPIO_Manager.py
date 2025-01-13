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
    -   __signal_GPIO_Shelly_power: Shelly功率
    -   __signal_GPIO_Shelly_power_factor: Shelly功率因数
    -   __signal_GPIO_Shelly_current: Shelly电流
    -   __signal_GPIO_Shelly_voltage: Shelly电压
    -   __signal_GPIO_Shelly_total: Shelly已充电Wh数
    -   __signal_GPIO_Shelly_total_returned: Shelly返回充电桩的总能量
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
        self.__signal_GPIO_Shelly_power = XSignal()
        self.__signal_GPIO_Shelly_power_factor = XSignal()
        self.__signal_GPIO_Shelly_current = XSignal()
        self.__signal_GPIO_Shelly_voltage = XSignal()
        self.__signal_GPIO_Shelly_total = XSignal()
        self.__signal_GPIO_Shelly_total_returned = XSignal()

        self.evse.signal_EVSE_min_current.connect(self.signal_GPIO_min_current.emit)
        self.evse.signal_EVSE_actual_current.connect(self.signal_GPIO_actual_current.emit)
        self.evse.signal_EVSE_failure.connect(self.signal_GPIO_EVSE_failure.emit)
        self.evse.signal_vehicle_state.connect(self.signal_GPIO_vehicle_state.emit)
        self.shelly.signal_Shelly_error.connect(self.signal_GPIO_Shelly_error.emit)
        self.shelly.signal_Shelly_power.connect(self.signal_GPIO_Shelly_power.emit)
        self.shelly.signal_Shelly_pf.connect(self.signal_GPIO_Shelly_power_factor.emit)
        self.shelly.signal_Shelly_current.connect(self.signal_GPIO_Shelly_current.emit)
        self.shelly.signal_Shelly_voltage.connect(self.signal_GPIO_Shelly_voltage.emit)
        self.shelly.signal_Shelly_total.connect(self.signal_GPIO_Shelly_total.emit)
        self.shelly.signal_Shelly_total_returned.connect(self.signal_GPIO_Shelly_total_returned.emit)

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
    def signal_GPIO_Shelly_power(self):
        return self.__signal_GPIO_Shelly_power

    @property
    def signal_GPIO_Shelly_power_factor(self):
        return self.__signal_GPIO_Shelly_power_factor

    @property
    def signal_GPIO_Shelly_current(self):
        return self.__signal_GPIO_Shelly_current

    @property
    def signal_GPIO_Shelly_voltage(self):
        return self.__signal_GPIO_Shelly_voltage

    @property
    def signal_GPIO_Shelly_total(self):
        return self.__signal_GPIO_Shelly_total

    @property
    def signal_GPIO_Shelly_total_returned(self):
        return self.__signal_GPIO_Shelly_total_returned


    def set_current(self,current):
        self.evse.set_current(current)

