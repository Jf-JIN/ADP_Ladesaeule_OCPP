

from const.Const_Parameter import *


from ._import_modbus_gpio import *
import typing
import threading


_log = Log.GPIO


class StructLED:
    __leds_name_list__ = set()

    def __init__(self, name: str, pin: int) -> None:
        if name in self.__leds_name_list__:
            _log.error(f'LED name {name} already exists')
            raise Exception(f'LED name {name} already exists')
        self.__pin = pin
        self.__name = name
        self.__led = LED(pin)
        self.__led.off()
        self.__status = False
        self.__blink_led_status = False
        self.__shouldBlink = False
        self.__blink_plan = 1
        self.__class__.__leds_name_list__.add(name)
        self.__blink_thread = threading.Timer(1, self.__blink)

    @property
    def status(self) -> bool:
        return self.__status

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pin(self) -> int:
        return self.__pin

    def set_enable(self, enable: bool) -> typing.Self:
        _log.debug(f'LED {self.__name} set_enable {self.__status} shouldBlink {self.__shouldBlink}')
        if enable and not self.__status:
            self.__status = True
            if not self.__shouldBlink:
                self.__led.on()
            else:
                self.__blink_led_status = False
                self.__blink(self.__blink_plan)
        elif not enable and self.__status:
            self.__shouldBlink = False
            self.__status = False
            self.__blink_led_status = False
            self.__led.off()
        return self

    def __blink(self, speed_s: float | int | list = 1) -> typing.Self:
        if not isinstance(speed_s, (float, int, list)):
            raise TypeError(f'blink speed must be float or int or list, not {type(speed_s)} and greater than 0, not {speed_s}')
        if isinstance(speed_s, list):
            speed_single = speed_s[0]
            if not isinstance(speed_single, (float, int)):
                raise TypeError(f'blink single speed must be float or int, not {type(speed_single)} and greater than 0, not {speed_single}')
            speed_list = speed_s
            speed_list.append(speed_list.pop(0))
        else:
            speed_single = speed_s
            speed_list = [speed_single]
        if speed_single <= 0:
            raise ValueError(f'blink speed must be greater than 0, not {speed_s}')
        _log.debug(f'in __blink __shouldBlink {self.__shouldBlink} {speed_s}')
        if self.__shouldBlink and self.__status:
            _log.debug(f'in __blink __blink_led_status {self.__blink_led_status}')
            if not self.__blink_led_status:
                _log.debug('led_on')
                self.__led.on()
                self.__blink_led_status = True
            else:
                _log.debug('led_off')
                self.__led.off()
                self.__blink_led_status = False
            _log.debug('set blink thread')
            if self.__blink_thread.is_alive():
                self.__blink_thread.cancel()
            _log.debug(speed_single, speed_list)
            self.__blink_thread = threading.Timer(speed_single, self.__blink, (speed_list,))
            self.__blink_thread.name = f'blink_{self.__name}'
            self.__blink_thread.start()
            _log.debug('start blink thread')
        return self

    def set_enable_blink(self, enable: bool, apply_now: bool = False, speed_s: int | float | list = 1) -> typing.Self:
        self.__shouldBlink: bool = enable
        if not enable:
            if self.__blink_thread.is_alive():
                self.__blink_thread.cancel()
            self.__blink_plan = 1
            self.__blink_led_status = False
            self.set_enable(enable)
            return self
        if apply_now:
            self.set_enable(enable)
            if self.__blink_plan == speed_s:
                return
            self.__blink_plan = speed_s
            self.__blink_led_status = False
            self.__blink(speed_s)
        return self


class ExclusiveGroupLED:
    __group_name_list__ = set()

    def __init__(self, name: str,  *leds: StructLED) -> None:
        if name in self.__group_name_list__:
            _log.error(f'ExclusiveGroupLED name {name} already exists')
            raise Exception(f'ExclusiveGroupLED name {name} already exists')
        self.__name = name
        self.__class__.__group_name_list__.add(name)
        self.__leds_dict_index = {}
        self.__leds_dict_name = {}
        for idx, led in enumerate(leds):
            if isinstance(led, StructLED):
                self.__leds_dict_index[idx] = led
                self.__leds_dict_name[led.name] = led
        self.__active_index = -1

    @property
    def active_led(self) -> int:
        return self.__active_index

    @property
    def name(self) -> str:
        return self.__name

    def add_led(self, led: StructLED) -> typing.Self:
        if isinstance(led, StructLED):
            if led.name not in self.__leds_dict_name:
                self.__leds_dict_index[len(self.__leds_dict_index)] = led
                self.__leds_dict_name[led.name] = led
            else:
                _log.warning(f"LED {led.name} already exists in the group")
        else:
            _log.warning(f"Invalid LED {led}, led must be an instance of StructLED")
        return self

    def remove_led(self, led: StructLED) -> typing.Self:
        if isinstance(led, StructLED):
            if led.name in self.__leds_dict_name:
                del self.__leds_dict_name[led.name]
                for idx, led in self.__leds_dict_index.items():
                    if led.name == led.name:
                        if idx == self.__active_index:
                            self.__active_index = -1
                        led.set_enable(False)
                        del self.__leds_dict_index[idx]
                        break
            else:
                _log.warning(f"LED {led.name} does not exist in the group")
        else:
            _log.warning(f"Invalid LED {led}, led must be an instance of StructLED")
        return self

    def clear(self) -> typing.Self:
        self.__active_index = -1
        for led in self.__leds_dict_index.values():
            led: StructLED
            led.set_enable(False)
        self.__leds_dict_index.clear()
        self.__leds_dict_name.clear()
        return self

    def get_led(self, led: int | str) -> StructLED | None:
        if isinstance(led, int):
            return self.__leds_dict_index.get(led, None)
        elif isinstance(led, str):
            return self.__leds_dict_name.get(led, None)
        else:
            return None

    def set_enable(self, led: int | str | None) -> typing.Self:
        if isinstance(led, int):
            self.__activate_index(led)
        elif isinstance(led, str):
            self.__activate_name(led)
        else:
            self.__activate_index(-1)
            _log.warning(f"LED <{led}> name or index is not valid, leds are disabled")
        return self

    def set_enable_blink(self, enable: bool, speed_s: int | float | list = 1) -> typing.Self:
        for led in self.__leds_dict_index.values():
            led: StructLED
            led.set_enable_blink(enable, speed_s)
        return self

    def __activate_name(self, led_name: str) -> None:
        self.__active_index = -1
        for idx, (name, led) in enumerate(self.__leds_dict_name.items()):
            led: StructLED
            if name == led_name:
                led.set_enable(True)
                self.__active_index = idx
            else:
                led.set_enable(False)

    def __activate_index(self, led_index: int) -> None:
        self.__active_index = -1
        for idx, led in self.__leds_dict_index.items():
            led: StructLED
            if idx == led_index:
                led.set_enable(True)
                self.__active_index = idx
            else:
                led.set_enable(False)


class ManagerLED:
    __instance__ = None

    def __new__(cls, *args, **kwargs) -> 'ManagerLED':
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(self) -> None:
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True
        self.__leds_dict_name: dict = {}
        self.__leds_dict_index: dict = {}
        self.__groups_dict_name: dict = {}

    def __register_led(self, name: str, pin: int) -> typing.Self:
        if name in self.__leds_dict_name or pin in self.__leds_dict_index:
            _log.warning(f"LED {name} already registered, skipped")
            return self
        led = StructLED(name, pin)
        self.__leds_dict_index[len(self.__leds_dict_index)] = led
        self.__leds_dict_name[name] = led
        return self

    def __register_group(self, group_name: str, led_name: str, led_pin: int) -> typing.Self:
        if group_name not in self.__groups_dict_name:
            self.__groups_dict_name[group_name] = ExclusiveGroupLED(group_name)
        group: ExclusiveGroupLED = self.__groups_dict_name[group_name]
        led = StructLED(led_name, led_pin)
        group.add_led(led)
        return self

    def __get_led(self, name: str) -> StructLED:
        return self.__leds_dict_name.get(name, None)

    def __get_group(self, name: str) -> ExclusiveGroupLED:
        return self.__groups_dict_name.get(name, None)

    def __shutdown(self) -> None:
        for led in self.__leds_dict_index.values():
            led: StructLED
            led.set_enable(False)
        for group in self.__groups_dict_name.values():
            group: ExclusiveGroupLED
            group.set_enable(-1)

    @staticmethod
    def registerLed(name: str, pin: int) -> "ManagerLED":
        instance = ManagerLED()
        return instance.__register_led(name, pin)

    @staticmethod
    def registerGroup(group_name: str, led_name: str, led_pin: int) -> "ManagerLED":
        instance = ManagerLED()
        return instance.__register_group(group_name, led_name, led_pin)

    @staticmethod
    def getLed(name: str) -> StructLED:
        instance = ManagerLED()
        return instance.__get_led(name)

    @staticmethod
    def getGroup(name: str) -> ExclusiveGroupLED:
        instance = ManagerLED()
        return instance.__get_group(name)

    @staticmethod
    def shutdown() -> None:
        instance = ManagerLED()
        instance.__shutdown()


MLED: typing.TypeAlias = ManagerLED
