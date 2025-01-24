#!/usr/bin/python
# -*- coding: utf-8 -*-
from gpiozero import LED
from const.GPIO_Parameter import GPIOParams
import time

class LatchMotor:
    def __init__(self,id):

        self.__id = None
        self.__isLocked = None
        self.__status_pin_lock = None
        self.__status_pin_unlock = None
        self.__lock_pin = LED(GPIOParams.GPIO_PIN_17)
        self.__unlock_pin = LED(GPIOParams.GPIO_PIN_27)



    @property
    def id(self):
        return self.__id

    @property
    def isLocked(self):
        return self.__isLocked

    def lock(self, ):
        self.__unlock_pin.off()
        self.__status_pin_unlock = False
        time.sleep(0.5)
        self.__lock_pin.on()
        self.__isLocked = True
        self.__status_pin_lock = True

    def unlock(self, ):
        self.__lock_pin.off()
        self.__status_pin_lock = False
        time.sleep(0.5)
        self.__unlock_pin.on()
        self.__isLocked = False
        self.__status_pin_unlock = True

    def stop(self):
        self.__lock_pin.off()
        self.__unlock_pin.off()

