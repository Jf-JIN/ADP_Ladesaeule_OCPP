from DToolslib import *
from Socket_Core import *
from const.Const_Logger import *
from PyQt5.QtCore import pyqtSignal


class SocketClient(SocketCore):
    signal_recv = EventSignal(dict)
    signal_error_output = EventSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        ...

    def connect(self):
        ...

    def disconnect(self):
        ...

    def send(self, data):
        ...
