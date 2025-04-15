
# from __future__ import annotations
import threading

# from gpiozero import LED  # 用于正常使用
from ._LED import LED  # 用于测试
from const.GPIO_Parameter import *
from const.Const_Parameter import *
from const.Const_Logger import *


_log = Log.GPIO


class LatchMotor:
    """
    数值默认正数是上锁
    """
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized = False
        return cls.__instance__

    def __init__(self) -> None:
        if self.__isInitialized:
            return
        self.__isInitialized = True
        _log.info('chushihua')
        # self.__id: int = id
        # self.__parent = None
        # self.__data_collector: DataCollector = DataCollector()
        self.__isLocked: bool = False  # 锁的状态, 是否是上锁状态
        self.__isRunning: bool = False  # 是否电机正在运行, 用于避免电机转动时, 动作冲突
        self.__command_list: list = []  # 存储命令的列表
        self.__status_pin_lock: bool = False  # 电机上锁控制引脚的状态, 可表示电机是否在正转
        self.__status_pin_unlock: bool = False  # 电机解锁控制引脚的状态, 可表示电机是否在反转
        self.__lock_pin: LED = LED(RaspPins.BCM_PIN_23)  # 电机上锁控制引脚
        self.__unlock_pin: LED = LED(RaspPins.BCM_PIN_22)  # 电机解锁控制引脚
        self.__timer: threading.Timer = threading.Timer(99, self.__off_lock_pin)
        self.__timer_intervall: int | float = GPIOParams.LETCH_MOTOR_RUNTIME  # 引脚状态转换的时间
        self.unlock(2)
        _log.info('jieshu')

    # @property
    # def id(self) -> int:
    #     return self.__id

    @property
    def isLocked(self) -> bool:
        return self.__isLocked

    @property
    def status_pin_lock(self) -> bool:
        return self.__status_pin_lock

    @property
    def status_pin_unlock(self) -> bool:
        return self.__status_pin_unlock

    def lock(self, timer_intervall) -> None:
        """
        上锁操作
        """
        _log.info("lock start")
        if self.__isRunning:
            self.__command_list.append(1)  # 正数表示上锁
        self.__timer_intervall = timer_intervall
        if self.__isLocked or self.__timer_intervall <= 0:
            _log.info(f"lock failed_already locked({self.__isLocked}) or intrvall too short({self.__timer_intervall}s)")
            return
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__lock_pin.on()
        self.__status_pin_lock = True
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_lock_pin)
        _log.info("lock success")
        self.__timer.start()

    def unlock(self, timer_intervall=GPIOParams.LETCH_MOTOR_RUNTIME) -> None:
        """
        解锁操作
        """
        _log.info("unlocking")
        if self.__isRunning:
            self.__command_list.append(-1)  # 负数表示解锁
        self.__timer_intervall = timer_intervall
        if not self.__isLocked or self.__timer_intervall <= 0:
            _log.info(f"lock failed_already locked({self.__isLocked}) or intrvall too short({self.__timer_intervall}s)")
            return
        self.__unlock_pin.on()
        self.__status_pin_unlock = True
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_unlock_pin)
        _log.info("unlocked")

    def stop(self) -> None:
        self.__lock_pin.off()
        self.__unlock_pin.off()
        # 缺少安全措施, 比如锁在一半停下了, 可以置默认操作, 上锁或解锁

    def __off_lock_pin(self) -> None:
        """
        一段时间后将上锁正转引脚置否, 停止电机运转
        """
        _log.info("lock_pin_closed")
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__isLocked = True
        self.__handle_signal_action_finished()

    def __off_unlock_pin(self) -> None:
        """
        一段时间后将解锁反转引脚置否, 停止电机运转
        """
        _log.info("unlock_pin_closed")
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__isLocked = False
        self.__handle_signal_action_finished()

    def __handle_signal_action_finished(self) -> None:
        """
        处理动作完成信号, 检查是否有后续连续操作
        """
        # self.__data_collector.set_CU_isLatched(id=self.id, flag=self.__isLocked)
        _log.info(f'Action finished, isLatched: {self.__isLocked}')
        # setattr(self.__parent, f'_{self.__parent.__class__.__name__}__isLatched', self.__isLocked)
        if len(self.__command_list) == 0:
            return
        command = self.__command_list.pop(0)
        if command > 0:
            self.lock()
        else:
            self.unlock()
