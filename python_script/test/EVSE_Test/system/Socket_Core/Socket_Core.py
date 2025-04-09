from socket import *
from socket import socket
from threading import Thread
from DToolslib import LogLevel, StaticEnum, Logger
from const.Const_Logger import *
from const.Const_Parameter import *
import json
import time

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
        return '_null in Socket_Core'


_Null = _null()


class _SocketThread(Thread):
    signal_connection_status = EventSignal(bool)
    signal_recv_json = EventSignal(dict)
    signal_recv = EventSignal(str)

    def __init__(self, parent, socket_obj: socket, host: str, port: int, isServer: bool = False) -> None:
        super().__init__()
        self.__parent: SocketCore = parent
        self.__socket_obj: socket = socket_obj
        self.__host: str = host
        self.__port: int = port
        self.__isServer: bool = isServer
        self.__isRunning = False

    def __del__(self) -> None:
        self.stop()

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def set_host(self, host: str) -> '_SocketThread':
        self.__host = host

    def set_port(self, port: int) -> '_SocketThread':
        self.__port = port

    def stop(self) -> None:
        self.__isRunning = False

    def connect(self, shouldCloseSocket: bool = False) -> bool:
        if shouldCloseSocket and hasattr(self, '__socket_obj'):
            try:
                self.__socket_obj.close()  # 如果 socket 已存在，关闭它
            except Exception:
                pass
        while self.__isRunning:
            try:
                self.__socket_obj = self.__parent.get_socket()
                if self.__isServer:
                    self.__socket_obj.bind((self.__host, self.__port))
                    self.__socket_obj.listen(SocketEnum.MAX_CONNECT)
                    self.signal_connection_status.emit(True)
                    _log.info('建立服务器成功')
                    return True
                else:
                    self.__socket_obj.connect((self.__host, self.__port))
                    self.signal_connection_status.emit(True)
                    _log.info(f'成功连接到服务器 {self.__host}:{self.__port}')
                    return True

            except (ConnectionRefusedError, ConnectionAbortedError, TimeoutError) as _:  # WinError 10061 由于目标计算机积极拒绝, 无法连接。
                _log.exception('The connection was rejected or time out, try to reconnect...')
                time.sleep(0.1)

            except (ConnectionResetError, OSError) as _:  # WinError 10054
                _log.exception('The connection is reset, and the other party may have closed the connection')
                self.signal_connection_status.emit(False)
                if hasattr(self, '__socket_obj'):
                    self.__socket_obj.close()

            except BlockingIOError as _:
                _log.exception('Non-blocking socket No data to read')
                time.sleep(0.1)

            except Exception as _:
                _log.exception('Unknown exception')
                self.signal_connection_status.emit(False)
                time.sleep(0.1)
        return False

    def receive_decode(self) -> None:
        try:
            data: bytes = self.__socket_obj.recv(SocketEnum.BUFFER_SIZE)

            if not data:
                _log.warning('连接断开：接收到空数据')
                self.signal_connection_status.emit(False)
                self.connect()
                return None

            try:
                decoded_data = data.decode()
            except UnicodeDecodeError as _:
                _log.exception('Data decoding failed')
                return None

            try:
                json_data: dict = json.loads(decoded_data)
                self.signal_recv_json.emit(json_data)
            except json.JSONDecodeError:
                pass
            self.signal_recv.emit(decoded_data)
            return None

        except (ConnectionResetError, ConnectionAbortedError, OSError) as _:
            _log.exception(f'Connection exception')
            self.signal_connection_status.emit(False)
            self.connect(shouldCloseSocket=True)

        except Exception as _:
            _log.exception(f'Unknown error')
            self.signal_connection_status.emit(False)
            self.connect(shouldCloseSocket=True)

    def run(self) -> None:
        self.__isRunning = True
        while self.__isRunning:
            data = self.__socket_obj.recv(1024)
            if not data:
                break
            print(data)


class SocketCore:
    signal_connection_status = EventSignal(bool)
    signal_error_output = EventSignal(str)

    def __init__(self, host: str, port: int, isServer: bool = False) -> None:
        self.__host = host
        self.__port = port
        self.__isServer = isServer
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__isConnected = False
        self.__thread_socket = _SocketThread(self, self.__socket, self.__host, self.__port, self.__isServer)
        self.__thread_socket.signal_connection_status.connect(self._set_connection_status)
        self.__thread_socket.signal_connection_status.connect(self.signal_connection_status)

    @property
    def isConnected(self) -> bool:
        return self.__isConnected

    def get_socket(self) -> socket:
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return self.__socket

    def _set_connection_status(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError('status must be bool')
        self.__isConnected = status

    def send(self, data: dict, client_socket: socket = _Null) -> bool:
        if not isinstance(data, dict):
            _log.warning('Failed to send data: data must be dict')
            return False

        if self.__isServer:
            if isinstance(client_socket, _null):
                client_list = []
                isSucceeded = True
                for client in client_list:
                    client: socket
                    result: bool = self.__send_chunked_data(data, client)
                    isSucceeded: bool = isSucceeded and result
                return isSucceeded
            elif isinstance(client_socket, socket):
                return self.__send_chunked_data(data, client_socket)
            else:
                _log.warning('Failed to send data: client_socket must be socket or _Null')
                return False
        else:
            return self.__send_chunked_data(data)

    def __send_chunked_data(self, data: dict, client_socket: socket = _Null) -> bool:
        if not self.__isConnected:
            _log.info(f'Socket is not connected')
            return False
        try:
            serialized_data = json.dumps(data)
            total_bytes = len(serialized_data)
            num_chunks = total_bytes // SocketEnum.BUFFER_SIZE + 1
            client_socket.sendall(num_chunks.to_bytes(SocketEnum.SLICE_SIZE, byteorder='big'))
            for i in range(num_chunks):
                start_idx = i * SocketEnum.BUFFER_SIZE
                end_idx = min((i + 1) * SocketEnum.BUFFER_SIZE, total_bytes)
                chunk = serialized_data[start_idx:end_idx]
                client_socket.sendall(chunk.encode())
            return
        except Exception as _:
            _log.exception()
            return False

    def connect(self, host: str = _Null, port: int = _Null) -> None:
        if self.__thread_socket.isRunning:
            _log.info(f'Socket is already connected with server({self.__host}:{self.__port})')
            return
        if not isinstance(host, (str, _null)) or not isinstance(port, (int, _null)):
            raise TypeError('host must be str and port must be int')
        self.__host: str = host
        self.__port: int = port
        self.__thread_socket.set_host(host).set_port(port)
        self.__thread_socket.start()

    def disconnect(self) -> None:
        if self.__isServer:
            for client in self.__thread_socket.clients_list:
                client[0].close()
            self.__thread_socket.clear_clients_list()
        else:
            self.__thread_socket.stop()
        self.__socket.close()
        self.__thread_socket.join()
        self.__isConnected = False

    def __del__(self) -> None:
        self.disconnect()
