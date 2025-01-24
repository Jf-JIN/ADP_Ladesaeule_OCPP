#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading

from gpiozero import LED

from const import RaspPins
from const.GPIO_Parameter import GPIOParams
import time

from sys_basis.XSignal import XSignal


class LatchMotor:
    """
    数值默认正数是上锁

    """
    def __init__(self,id:int)->None:
        self.__id:int = id
        self.__isLocked:bool = False # 锁的状态，是否是上锁状态
        self.__isRunning:bool = False # 是否电机正在运行，用于避免电机转动时，动作冲突
        self.__command_list:list = [] # 存储命令的列表
        self.__status_pin_lock:bool = False # 电机上锁控制引脚的状态，可表示电机是否在正转
        self.__status_pin_unlock:bool = False # 电机解锁控制引脚的状态，可表示电机是否在反转
        self.__lock_pin:LED = LED(23) # 电机上锁控制引脚
        self.__unlock_pin:LED = LED(24) # 电机解锁控制引脚
        self.__timer:threading.Timer = threading.Timer(99, self.__off_lock_pin)
        self.__timer_intervall:int|float = 2 # 引脚状态转换的时间



    @property
    def id(self)->int:
        return self.__id

    @property
    def isLocked(self)->bool:
        return self.__isLocked

    def lock(self)->None:
        """
        上锁操作
        """
        if self.__isRunning:
            self.__command_list.append(1)
        if self.__isLocked:
            return
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__lock_pin.on()
        self.__status_pin_lock = True
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_lock_pin)

    def unlock(self)->None:
        """
        解锁操作
        """
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__unlock_pin.on()
        self.__isLocked = False
        self.__status_pin_unlock = True
        self.__timer = threading.Timer(self.__timer_intervall, self.__off_unlock_pin)

    def stop(self)->None:
        self.__lock_pin.off()
        self.__unlock_pin.off()

    def __off_lock_pin(self)->None:
        """
        一段时间后将上锁正转引脚置否，停止电机运转
        """
        self.__lock_pin.off()
        self.__status_pin_lock = False
        self.__isLocked = True
        self.__handle_signal_action_finished()

    def __off_unlock_pin(self)->None:
        """
        一段时间后将解锁反转引脚置否，停止电机运转
        """
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        self.__isLocked = False
        self.__handle_signal_action_finished()

    def __handle_signal_action_finished(self)->None:
        """
        处理动作完成信号, 检查是否有后续连续操作
        """
        if len(self.__command_list) == 0:
            return
        command = self.__command_list.pop(0)
        if command > 0:
            self.lock()
        else:
            self.unlock()