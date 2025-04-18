from __future__ import annotations
from threading import Thread
from ._Modbus_IO import ModbusIO
from const.GPIO_Parameter import *
from const.Const_Parameter import *
import time
from ._import_modbus_gpio import *
from DToolslib import Inner_Decorators


if 0:
    from ._GPIO_Manager import GPIOManager
    from ._Charge_Unit import ChargeUnit
    from ._Data_Collector import DataCollector
    from ._EVSE import Evse

_log = Log.EVSE


class PollingEVSE(Thread):
    def __init__(self, parent: GPIOManager, charge_unit_dict: dict, intervall: int | float) -> None:
        super().__init__(name='PollingEVSE')
        self.__parent: GPIOManager = parent
        self.__evse_list: list = []
        for item in charge_unit_dict.values():
            item: ChargeUnit
            self.__evse_list.append(item.evse)
        self.__evse_quantity: int = len(self.__evse_list)
        self.__interval: int | float = intervall
        self.__data_collector: DataCollector = self.__parent.data_collector
        self.__isRunning: bool = True
        self.__current_index: int = 0

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    # @Inner_Decorators.time_counter
    # def __get_watching_registers_dict(self, io: ModbusIO) -> dict:
    #     temp = {}
    #     for register_address in GPIOParams.WATCHING_REGISTERS:
    #         subtmp = {}
    #         ModbusPDU_res: ModbusPDU = io.read_PDU(register_address)
    #         if ModbusPDU_res is None:
    #             temp[str(register_address)] = {}
    #             _log.warning(f'EVSE <{register_address}> read error')
    #             continue
    #         isError: bool = ModbusPDU_res.isError()
    #         subtmp['function_code'] = ModbusPDU_res.function_code
    #         subtmp['registers'] = ModbusPDU_res.registers
    #         subtmp['status'] = ModbusPDU_res.status
    #         subtmp['isError'] = isError
    #         subtmp['exception_code'] = ModbusPDU_res.exception_code if isError else 0
    #         subtmp['dev_id'] = ModbusPDU_res.dev_id
    #         subtmp['transaction_id'] = ModbusPDU_res.transaction_id
    #         subtmp['bits'] = ModbusPDU_res.bits
    #         subtmp['address'] = ModbusPDU_res.address
    #         temp[str(register_address)] = subtmp
    #     return temp

    # @Inner_Decorators.time_counter
    def __get_watching_registers_dict(self, io: ModbusIO) -> dict:
        temp = {}
        for (register_address, register_length) in GPIOParams.WATCHING_REGISTERS_GROUP:
            ModbusPDU_res: ModbusPDU | ExceptionResponse = io.read_PDU(register_address, register_length)
            if ModbusPDU_res is None or ModbusPDU_res.isError():
                # temp[str(register_address)] = {}
                _log.warning(f'EVSE <{register_address}> read error')
                continue
            for index, value in enumerate(ModbusPDU_res.registers):
                act_address = register_address + index
                subtmp = {}
                if act_address not in GPIOParams.WATCHING_REGISTERS:
                    continue
                isError: bool = ModbusPDU_res.isError()
                subtmp['function_code'] = ModbusPDU_res.function_code
                subtmp['registers'] = value
                subtmp['status'] = ModbusPDU_res.status
                subtmp['isError'] = isError
                subtmp['exception_code'] = ModbusPDU_res.exception_code if isError else 0
                subtmp['dev_id'] = ModbusPDU_res.dev_id
                subtmp['transaction_id'] = ModbusPDU_res.transaction_id
                subtmp['bits'] = ModbusPDU_res.bits
                subtmp['address'] = ModbusPDU_res.address
                temp[str(act_address)] = subtmp
        return temp

    def run(self) -> None:
        while self.__isRunning:
            evse: Evse = self.__evse_list[self.__current_index]
            evse_id: int = evse.id
            evse_data = {}
            with ModbusIO(id=evse_id) as io:
                # _log.info(f'EVSE <{evse_id}> polling 1')
                evse_data.update(self.__get_watching_registers_dict(io))
                # _log.info(f'EVSE <{evse_id}> polling 2')
                vehicle_state: int | None = io.read_vehicle_status()  # timeout 由 Modbus 决定
                # _log.info(f'EVSE <{evse_id}> polling 3')
                if vehicle_state is not None:
                    # _log.info(f'EVSE <{evse_id}> polling 4')
                    evse_data['vehicle_state'] = vehicle_state
                    evse.set_vehicle_state(vehicle_state)
                    # _log.info(f'EVSE <{evse_id}> polling 5')

                evse_error: None | set = io.read_evse_status_fails()
                # _log.info(f'EVSE <{evse_id}> polling 6')
                if evse_error is not None:
                    # _log.info(f'EVSE <{evse_id}> polling 7')
                    evse_data['evse_error'] = evse_error
                    evse.set_evse_status_error(evse_error)
                    # _log.info(f'EVSE <{evse_id}> polling 8')
                else:
                    _log.error(f'EVSE {evse_id} read error')
                #     _log.info(f'EVSE <{evse_id}> polling 9')
                # _log.info(f'EVSE <{evse_id}> polling 10')
                if len(evse_data):
                    # _log.info(f'EVSE <{evse_id}> polling 11')
                    self.__data_collector.set_evse_data(evse_id, evse_data)
                    # _log.info(f'EVSE <{evse_id}> polling 12')
            # _log.info(f'EVSE <{evse_id}> polling 13')
            self.__current_index = (self.__current_index + 1) % self.__evse_quantity
            # _log.info(f'EVSE <{evse_id}> polling 14')
            time.sleep(self.__interval)
            # _log.info(f'EVSE <{evse_id}> polling 15')

    def stop(self) -> None:
        self.__isRunning = False
        self.join()
