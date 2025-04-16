
from __future__ import annotations
import threading

from ._import_modbus_gpio import *
from const.GPIO_Parameter import *
from const.Const_Parameter import *

if 0:
    from ._Data_Collector import DataCollector
    from ._Charge_Unit import ChargeUnit

_info = Log.GPIO.info


class LatchMotor:
    """
    数值默认正数是上锁
    """

    def __init__(self, parent: ChargeUnit, id: int) -> None:
        self.__id: int = id
        self.__parent: ChargeUnit = parent
        self.__data_collector: DataCollector = parent.parent_obj.data_collector
        self.__isLocked: bool = False  # 锁的状态, 是否是上锁状态
        self.__isRunning: bool = False  # 是否电机正在运行, 用于避免电机转动时, 动作冲突
        self.__command_list: list = []  # 存储命令的列表
        self.__status_pin_lock: bool = False  # 电机上锁控制引脚的状态, 可表示电机是否在正转
        self.__status_pin_unlock: bool = False  # 电机解锁控制引脚的状态, 可表示电机是否在反转
        self.__lock_pin: LED = LED(RaspPins.BCM_PIN_23)  # 电机上锁控制引脚
        self.__unlock_pin: LED = LED(RaspPins.BCM_PIN_22)  # 电机解锁控制引脚
        self.__timer: threading.Timer = threading.Timer(99, self.__off_lock_pin)
        self.__timer.name = 'LatchMotor'
        self.__timer_intervall: int | float = GPIOParams.LETCH_MOTOR_RUNTIME  # 引脚状态转换的时间

    @property
    def id(self) -> int:
        return self.__id

    @property
    def isLocked(self) -> bool:
        return self.__isLocked

    @property
    def status_pin_lock(self) -> bool:
        return self.__status_pin_lock

    @property
    def status_pin_unlock(self) -> bool:
        return self.__status_pin_unlock

    def lock(self) -> None:
        """
        上锁操作
        """
        if self.__isRunning:
            self.__command_list.append(1)  # 正数表示上锁
        if self.__isLocked or self.__timer_intervall <= 0:
            return
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__lock_pin.on()
        self.__status_pin_lock = True
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_lock_pin)
        self.__timer.name = 'LatchMotor'
        self.__timer.start()

    def unlock(self) -> None:
        """
        解锁操作
        """
        if self.__isRunning:
            self.__command_list.append(-1)  # 负数表示解锁
        if not self.__isLocked or self.__timer_intervall <= 0:
            return
        self.__unlock_pin.on()
        self.__status_pin_unlock = True
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_unlock_pin)
        self.__timer.name = 'LatchMotor'
        self.__timer.start()

    def stop(self) -> None:
        self.__lock_pin.off()
        self.__unlock_pin.off()
        # 缺少安全措施, 比如锁在一半停下了, 可以置默认操作, 上锁或解锁

    def __off_lock_pin(self) -> None:
        """
        一段时间后将上锁正转引脚置否, 停止电机运转
        """
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__isLocked = True
        self.__handle_signal_action_finished()

    def __off_unlock_pin(self) -> None:
        """
        一段时间后将解锁反转引脚置否, 停止电机运转
        """
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__isLocked = False
        self.__handle_signal_action_finished()

    def __handle_signal_action_finished(self) -> None:
        """
        处理动作完成信号, 检查是否有后续连续操作
        """
        self.__data_collector.set_CU_isLatched(id=self.id, flag=self.__isLocked)
        _info(f'Action finished, isLatched: {self.__isLocked}')
        setattr(self.__parent, f'_{self.__parent.__class__.__name__}__isLatched', self.__isLocked)
        if len(self.__command_list) == 0:
            return
        command = self.__command_list.pop(0)
        if command > 0:
            self.lock()
        else:
            self.unlock()
