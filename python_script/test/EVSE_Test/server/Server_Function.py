

from system.Socket_Core import *
from system.Modbus_Handler import *
from system.Latch_Motor import *

_log = Log.SERVER


class ServerFunction:
    def __init__(self):

        self.__init_parameters()
        self.__init_signal_connections()
        self.start()

    def __init_parameters(self) -> None:
        self.__socket_core = SocketCore('0.0.0.0', isServer=True)
        self.__modbus_handler = ModbusHandler()
        self.__LatchMotor = None
        self.__reflect_recv_dict = {
            'modbus_data_read': self.__modbus_data_read,
            'modbus_data_write': self.__modbus_data_write,
            'motor_run': self.__motor_run,
        }

    def __init_signal_connections(self) -> None:
        self.__socket_core.signal_recv_json.connect(self.__socket_recv_json)

    def start(self) -> None:
        self.__socket_core.connect()
        self.__modbus_handler.connect()

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
        _log.info(f'received read request: {recv_data}')
        modbus_id = recv_data.get('modbus_id', None)
        register_address = recv_data.get('read_request', None)
        isSpecific = recv_data.get('isSpecific', False)
        if modbus_id is None or register_address is None:
            return
        self.__modbus_handler.set_id(modbus_id)
        Modbus_PDU: None | ModbusDataStruct = self.__modbus_handler.read(register_address)
        _log.info(f'read result: "{Modbus_PDU}"')
        if Modbus_PDU is None:
            response = {
                'modbus_id': modbus_id,
                'register_address': register_address,
                'data': None,
                'isSpecific': isSpecific
            }
        else:
            data = Modbus_PDU.json_data
            response = {'modbus_data_read': {
                'modbus_id': modbus_id,
                'register_address': register_address,
                'data': data,
                'isSpecific': isSpecific
            }}
        result = self.__socket_core.send(response)
        if result:
            _log.info(f'sent response: {response}')
        else:
            _log.error(f'failed to send response: {response}')

    def __modbus_data_write(self, recv_data: dict) -> None:
        """ 
        {
            'modbus_id': modbus_id, 
            'write_request': [register_address, register_value]
        }
        """
        _log.info(f'received write request: {recv_data}')
        modbus_id = recv_data.get('modbus_id', None)
        request_data = recv_data.get('write_request', [])
        if modbus_id is None or len(request_data) != 2:
            return
        register_address = request_data[0]
        register_value = request_data[1]
        self.__modbus_handler.set_id(modbus_id)
        self.__modbus_handler.write(register_address, register_value)

    def __motor_run(self, recv_data: dict) -> None:
        """ 
        {
            'doLock': bool
        }
        """
        _log.info(f'received motor run request: {recv_data}')
        doLock = recv_data.get('doLock', None)
        runtime = recv_data.get('runtime', None)
        _log.info(f'doLock: {doLock}, runtime: {runtime}')
        if doLock is None or runtime is None:
            _log.warning(f'invalid motor run request: "{recv_data}"')
            return
        runtime = int(runtime)
        if doLock:
            self.__run_motor_lock(runtime)
        else:
            self.__run_motor_unlock(runtime)

    def __run_motor_lock(self, runtime):
        _log.info(f'run motor lock')
        if not self.__LatchMotor:
            _log.info('ddd')
            a = LatchMotor(self)
            _log.info(a)
            self.__LatchMotor = LatchMotor(self)

        _log.info(f'running motor lock for {runtime} seconds')
        self.__LatchMotor.lock(runtime)

    def __run_motor_unlock(self, runtime):
        _log.info(f'run motor unlock')
        if not self.__LatchMotor:
            self.__LatchMotor = LatchMotor(self)
        _log.info(f'running motor lock for {runtime} seconds')
        self.__LatchMotor.unlock(runtime)
