
from const.GPIO_Parameter import *
from gpiozero import LED
# from ._test_Module import LED


class StructLED:
    def __init__(self, pin: int, name: str):
        self.__pin = pin
        self.__name = name
        self.__led = LED(pin)
        self.__led.off()
        self.__status = False

    @property
    def status(self) -> bool:
        return self.__status

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pin(self) -> int:
        return self.__pin

    def set_enable(self, enable: bool):
        self.__status = enable
        if self.__status:
            self.__led.on()
        else:
            self.__led.off()


class GroupLED:
    def __init__(self, led1: StructLED, led2: StructLED):
        pass


class ManagerStatusLED:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(self):
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True
        self.__led_green = StructLED(RaspPins.BCM_PIN_23, 'Green')
        self.__led_red = StructLED(RaspPins.BCM_PIN_24, 'Rot')

    def set_led_green(self, value: bool):
        self.__led_green.set_enable(value)
        self.__led_red
