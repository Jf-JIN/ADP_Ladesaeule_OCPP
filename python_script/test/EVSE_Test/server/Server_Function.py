

from system.Socket_Core import *
from system.Modbus_Handler import *
import sys
import os
import signal
import atexit

_log = Log.SERVER


class ServerFunction:
    def __init__(self):

        self.__init_parameters()
        self.__init_signal_connections()
        self.start()

    def __init_parameters(self) -> None:
        self.__socket_core = SocketCore('0.0.0.0', isServer=True)
        self.__modbus = ModbusIO()
        self.__reflect_recv_dict = {
            'modbus_data_read': self.__modbus_data_read,
            'modbus_data_write': self.__modbus_data_write,
            'shutdown': self.__shutdown
        }

    def __init_signal_connections(self) -> None:
        self.__socket_core.signal_recv_json.connect(self.__isolate_socket_recv_json)

    def __isolate_socket_recv_json(self, recv_data: dict) -> None:
        self.__isolation_recv_json_timer = threading.Timer(0, self.__socket_recv_json, (recv_data,))
        self.__isolation_recv_json_timer.start()

    def start(self) -> None:
        self.__socket_core.connect()

    def __socket_recv_json(self, recv_data: dict) -> None:
        # _log.info(f'received request: {recv_data}')
        for key, value in recv_data.items():
            if key not in self.__reflect_recv_dict:
                continue
            self.__reflect_recv_dict.get(key, lambda x: None)(value)

    def __modbus_data_read(self, recv_data: dict) -> None:
        """ 
        {
            'modbus_id': modbus_id, 
            'read_request': register_address, 
            'isSpecific': isSpecific
        }
        """
        _log.info(f'[Read] request: {recv_data}')
        modbus_id = recv_data.get('modbus_id', None)
        register_address = recv_data.get('read_request', None)
        isSpecific = recv_data.get('isSpecific', False)
        if modbus_id is None or register_address is None:
            return
        self.__modbus.set_id(modbus_id)
        with self.__modbus as io:
            PDUStruct: ModbusDataStruct = io.read(register_address)
        response = {
            'modbus_id': modbus_id,
            'register_address': register_address,
            'data': PDUStruct.json_data,
            'isSpecific': isSpecific
        }
        result: bool = self.__socket_core.send({'modbus_data_read': response})
        # if result:
        #     _log.info(f'Succeeded[{register_address}]: {PDUStruct}')
        # else:
        #     _log.error(f'FAILED[{register_address}]: {PDUStruct}')

    def __modbus_data_write(self, recv_data: dict) -> None:
        """ 
        {
            'modbus_id': modbus_id, 
            'write_request': [register_address, register_value]
        }
        """
        _log.info(f'[Write] request: {recv_data}')
        modbus_id = recv_data.get('modbus_id', None)
        request_data = recv_data.get('write_request', [])
        if modbus_id is None or len(request_data) != 2:
            _log.error(f'Invalid write request: {recv_data}')
            return
        register_address = request_data[0]
        register_value = request_data[1]
        self.__modbus.set_id(modbus_id)
        with self.__modbus as io:
            io.write(register_address, register_value)

    def __shutdown(self, recv_data: dict) -> None:
        _log.info(f'[Shutdown] request: {recv_data}')
        shouldShutdown = recv_data.get('shouldShutDown', None)
        if shouldShutdown is None:
            _log.warning(f'invalid shutdown request: "{recv_data}"')
            return
        self.__socket_core.disconnect()
        os.kill(signal.SIGTERM, os.getpid())
        os._exit(0)
