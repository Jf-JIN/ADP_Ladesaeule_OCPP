from DToolslib import *
from Socket_Core import *
from const.ConstLogger import *
from PyQt5.QtCore import pyqtSignal


class SocketServer(SocketCore):
    signal_data_recv = EventSignal(dict)
    signal_error_output = EventSignal(str)

    def __init__(self) -> None:
        ...

    def connect(self):
        ...

    def disconnect(self):
        ...

    def send(self, data):
        ...
