

class LED:
    def __init__(self, pin):
        if pin == 23:
            self.__key = 'latch_lock_pin'
        elif pin == 22:
            self.__key = 'latch_unlock_pin'
        self.__fp = None

    def on(self):
        ...

    def off(self):
        ...


class Button:
    def __init__(self, pin, *args, **kwargs):
        self.__pin = pin
        self.__fp = ...

    def when_activated(self):
        ...


class RPi:
    class _GPIO:
        def setmode(arg):
            ...

        def setup(*args, **kwargs):
            ...

        def add_event_detect(*args, **kwargs):
            ...

    def __init__(self, *args, **kwargs):
        ...

    @staticmethod
    def GPIO():
        return RPi._GPIO
