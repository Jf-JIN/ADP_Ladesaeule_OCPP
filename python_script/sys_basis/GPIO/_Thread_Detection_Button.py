

from ._import_modbus_gpio import *
from threading import Thread
from const.Const_Parameter import *
from const.GPIO_Parameter import *
from DToolslib import *

_log = Log.GPIO


class DetectionButton(Thread):
    pressed = EventSignal(bool)

    def __init__(self, name: str, button: Button) -> None:
        super().__init__(name=f'DetectionButton<{name}>', daemon=True)
        self.__button: Button = button
        self.__isRunning = False
        self.__name = f'DetectionButton<{name}>'

    def run(self) -> None:
        self.__isRunning = True
        while self.__isRunning:
            self.__button.wait_for_active()
            if self.__isRunning:
                _log.debug(f'{self.__name} pressed')
                self.pressed.emit(True)
            self.__button.wait_for_inactive()

    def stop(self) -> None:
        self.__isRunning = False
        self.__button._active_event.set()
