

from __future__ import annotations
from socket import *
from threading import Thread
from const.Const_Logger import *
from const.Const_Parameter import *
import json
import time
import typing

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


class _ClientConnectionStruct:
    def __init__(self, socket_obj: socket, socket_address: tuple, recv_thread: Thread) -> None:
        self.__socket_obj: socket = socket_obj
        self.__socket_address: tuple = socket_address
        self.__recv_thread: Thread = recv_thread

    def __repr__(self) -> str:
        return f'_ClientConnectionStruct(\nsocket: {self.__socket_obj}, address: {self.__socket_address},\nthread: {self.__recv_thread})'

    @property
    def socket_obj(self) -> socket:
        return self.__socket_obj

    @property
    def socket_address(self) -> tuple:
        return self.__socket_address

    @property
    def recv_thread(self) -> '_ServerReceiveThread':
        return self.__recv_thread


class _ServerReceiveThread(Thread):
    def __init__(self, parent, socket_obj: socket, recv_func: typing.Callable) -> None:
        super().__init__()
        self.__parent: _SocketThread = parent
        self.__socket_obj: socket = socket_obj
        self.__recv_func: typing.Callable = recv_func
        self.__isRunning: bool = True

    @property
    def parent(self) -> '_SocketThread':
        return self.__parent

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def stop(self) -> None:
        self.__isRunning = False

    def run(self) -> None:
        while self.__isRunning:
            try:
                self.__recv_func(self.__socket_obj)
            except:
                pass
        self.__socket_obj.close()


class _SocketThread(Thread):
    signal_connection_status = EventSignal(bool)
    signal_recv_json = EventSignal(dict)
    signal_recv = EventSignal(str)

    def __init__(self, parent, socket_obj: socket, host: str = '0.0.0.0', port: int = SocketEnum.DEFAULT_PORT, isServer: bool = False) -> None:
        super().__init__()
        self.__parent: SocketCore = parent
        self.__socket_obj: socket = socket_obj
        self.__host: str = host
        self.__port: int = port
        self.__isServer: bool = isServer
        self.__isRunning = False
        self.__client_list = []

    def __del__(self) -> None:
        self.stop()

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    @property
    def clients_list(self) -> list:
        return self.__client_list

    def clear_clients_list(self) -> None:
        for client_struct in self.__client_list:
            client_struct: _ClientConnectionStruct
            client_struct.recv_thread.stop()
            client_struct.recv_thread.join()
            client_struct.socket_obj.close()
        self.__client_list.clear()

    def set_host(self, host: str) -> '_SocketThread':
        self.__host = host

    def set_port(self, port: int) -> '_SocketThread':
        self.__port = port

    def stop(self) -> None:
        self.__isRunning = False
        if not len(self.__client_list):
            self.clear_clients_list()

    def __connect_server(self) -> bool:
        if not self.__isServer:
            _log.warning('_SocketThread: __connect_server() is not available for client')
            return False
        while self.__isRunning:
            try:
                self.__socket_obj.bind((self.__host, self.__port))
                self.__socket_obj.listen(SocketEnum.MAX_CONNECT)
                self.signal_connection_status.emit(True)
                _log.info('Server establish success, waiting for clients')
                return True
            except Exception as _:
                _log.exception('Server establish failed')
                self.signal_connection_status.emit(False)
                time.sleep(1)
        return False

    def __connect_client(self, shouldCloseSocket: bool = False) -> bool:
        """ 
        用于客户端重连
        """
        if self.__isServer:
            _log.warning('_SocketThread: __connect_client() is not available for server')
            return False

        if shouldCloseSocket and hasattr(self, '__socket_obj'):
            try:
                self.__socket_obj.close()
            except Exception:
                pass

        while self.__isRunning:
            try:
                self.__socket_obj = self.__parent.get_socket()
                self.__socket_obj.connect((self.__host, self.__port))
                self.signal_connection_status.emit(True)
                _log.info(f'Successfully connected to {self.__host}:{self.__port}')
                return True

            except (ConnectionRefusedError, ConnectionAbortedError, TimeoutError) as _:  # WinError 10061
                # _log.exception('The connection was rejected or time out, try to reconnect...')
                time.sleep(0.1)

            except (ConnectionResetError, OSError) as _:  # WinError 10054
                # _log.exception('The connection is reset, and the other party may have closed the connection')
                self.signal_connection_status.emit(False)
                if hasattr(self, '__socket_obj'):
                    self.__socket_obj.close()

            except BlockingIOError as _:
                # _log.exception('Non-blocking socket No data to read')
                time.sleep(0.1)

            except Exception as _:
                # _log.exception('Unknown exception')
                self.signal_connection_status.emit(False)
                time.sleep(0.1)
        return False

    def __receive_decode(self, socket_obj: socket) -> None:
        try:
            data: bytes = socket_obj.recv(SocketEnum.BUFFER_SIZE)

            if not data:
                _log.warning('连接断开：接收到空数据')
                self.signal_connection_status.emit(False)
                self.__connect_client()
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
            if self.__isServer:
                socket_obj.close()
                return None
            # _log.exception(f'Connection exception')
            self.signal_connection_status.emit(False)
            self.__connect_client(shouldCloseSocket=True)

        except Exception as _:
            if self.__isServer:
                socket_obj.close()
                return None
            _log.exception(f'Unknown error')
            self.signal_connection_status.emit(False)
            self.__connect_client(shouldCloseSocket=True)

    def __server_connection_listening(self) -> None:
        if not self.__isServer:
            _log.warning(f'Cannot start server listening on {self.__host}:{self.__port} as this is not a server')
            return
        self.__connect_server()
        while self.__isRunning:
            try:
                client_socket, client_address = self.__socket_obj.accept()
                _log.info(f'{client_address} connected')
                recv_thread = _ServerReceiveThread(parent=self, socket_obj=client_socket, recv_func=self.__receive_decode)
                self.__client_list.append(_ClientConnectionStruct(socket_obj=client_socket, socket_address=client_address, recv_thread=recv_thread))
                recv_thread.start()
            except Exception as _:
                _log.exception('Connection listening error')
        self.clear_clients_list()
        self.stop()

    def __run_client_receiver(self) -> None:
        if self.__isServer:
            _log.warning('This is a server socket, cannot run client receiver')
            return
        self.__connect_client()
        while self.__isRunning:
            try:
                self.__receive_decode(self.__socket_obj)
            except:
                pass
        self.stop()

    def run(self) -> None:
        self.__isRunning = True
        if self.__isServer:
            self.__server_connection_listening()
        else:
            self.__run_client_receiver()


class SocketCore:
    signal_connection_status = EventSignal(bool)
    signal_recv_json = EventSignal(dict)
    signal_recv = EventSignal(str)

    def __init__(self, host: str, port: int = SocketEnum.DEFAULT_PORT, isServer: bool = False) -> None:
        self.__host = host
        self.__port = port
        self.__isServer = isServer
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__isConnected = False
        self.__thread_socket = _SocketThread(self, self.__socket, self.__host, self.__port, self.__isServer)
        self.__thread_socket.signal_connection_status.connect(self._set_connection_status)
        self.__thread_socket.signal_connection_status.connect(self.signal_connection_status.emit)
        self.__thread_socket.signal_recv_json.connect(self.signal_recv_json.emit)
        self.__thread_socket.signal_recv.connect(self.signal_recv.emit)

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
                client_list = self.__thread_socket.clients_list
                isSucceeded = True
                for client_struct in client_list:
                    client_struct: _ClientConnectionStruct
                    if client_struct.socket_obj.fileno() == -1:
                        client_struct.recv_thread.stop()
                        client_struct.recv_thread.join()
                        client_struct.socket_obj.close()
                        continue
                    result: bool = self.__send_chunked_data(data, client_struct.socket_obj)
                    isSucceeded: bool = isSucceeded and result
                return isSucceeded
            elif isinstance(client_socket, socket):
                return self.__send_chunked_data(data, client_socket)
            else:
                _log.warning('Failed to send data: client_socket must be socket or _Null')
                return False
        else:
            return self.__send_chunked_data(data, self.__socket)

    def __send_chunked_data(self, data: dict, client_socket: socket) -> bool:
        if not self.__isConnected or client_socket.fileno() == -1:
            # _log.info(f'Socket is not connected')
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
        if self.__isConnected:
            _log.info(f'Socket is already connected with server({self.__host}:{self.__port})')
            return
        if self.__thread_socket.isRunning:
            _log.info(f'Socket is already running')
            return
        if not isinstance(host, (str, _null)) or not isinstance(port, (int, _null)):
            raise TypeError('host must be str and port must be int')
        if not isinstance(host, _null) and not isinstance(port, _null):
            self.__host: str = host
            self.__port: int = port
            self.__thread_socket.set_host(host).set_port(port)
        self.__thread_socket.start()

    def disconnect(self) -> None:
        self.__thread_socket.stop()
        self.__socket.close()
        self.__thread_socket.join()
        self.__isConnected = False

    def __del__(self) -> None:
        self.disconnect()
