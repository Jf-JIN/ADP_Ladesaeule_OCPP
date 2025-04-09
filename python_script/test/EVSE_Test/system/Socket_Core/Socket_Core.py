from socket import *
from socket import socket
from threading import Thread
from DToolslib import LogLevel, StaticEnum, Logger
from const.Const_Logger import *

_log: Logger = Log.SOCKET


class _null:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized__ = False
        return cls.__instance__

    def __init__(self) -> None:
        if self.__isInitialized__:
            return
        self.__isInitialized__ = True

    def __repr__(self):
        return "_null in Socket_Core"


_Null = _null()


class SocketThread(Thread):
    signal_connection_status = EventSignal(bool)

    def __init__(self, socket_obj: socket, host: str, port: int) -> None:
        super().__init__()
        self.__socket_obj: socket = socket_obj
        self.__host: str = host
        self.__port: int = port
        self.__isRunning = False

    def __del__(self) -> None:
        self.stop()

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def stop(self) -> None:
        self.__isRunning = False

    def connect(self) -> bool:
        try:
            self.__socket_obj.bind((self.__host, self.__port))
            self.signal_connection_status.emit(True)
        except Exception as e:
            self.signal_connection_status.emit(False)
            _log.exception()

    def set_host(self, host: str) -> 'SocketThread':
        self.__host = host

    def set_port(self, port: int) -> 'SocketThread':
        self.__port = port

    def run(self) -> None:
        self.__isRunning = True
        while self.__isRunning:
            data = self.__socket_obj.recv(1024)
            if not data:
                break
            print(data)


class SocketCore:
    signal_connection_status = EventSignal(bool)

    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__isConnected = False
        self.__thread = SocketThread(self.__socket, self.__host, self.__port)
        self.__thread.signal_connection_status.connect(self._set_connection_status)
        self.__thread.signal_connection_status.connect(self.signal_connection_status)

    @property
    def isConnected(self) -> bool:
        return self.__isConnected

    def _set_connection_status(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError("status must be bool")
        self.__isConnected = status

    def send(self, data) -> None:
        if self.__isConnected:
            self.__socket.sendall(data)
        else:
            _log.info("Socket is not connected with server")

    def connect(self, host: str = _Null, port: int = _Null) -> None:
        if self.__thread.isRunning:
            _log.info(f"Socket is already connected with server({self.__host}:{self.__port})")
            return
        if not isinstance(host, (str, _null)) or not isinstance(port, (int, _null)):
            raise TypeError("host must be str and port must be int")
        self.__host: str = host
        self.__port: int = port
        self.__thread.set_host(host).set_port(port)
        self.__thread.start()

    def disconnect(self) -> None:
        self.__thread.stop()
        self.__socket.close()
        self.__thread.wait()
        self.__isConnected = False
