

from __future__ import annotations
import copy
from const.Const_Parameter import *
import requests
import time
from sys_basis.XSignal import XSignal

if 0:
    from _Charge_Unit import ChargeUnit

_log = Log.GPIO


class Shelly:
    def __init__(self, parent, id: int, address: str) -> None:
        self.__parent: ChargeUnit = parent
        self.__id: int = id
        self.__main_address: str = address if address.startswith('http') else f'http://{address}'
        self.__data: dict = {}
        self.__isAvailable: bool = False
        self.__charged_energy: int = 0
        self.__charged_energy_shelly: int = 0
        self.__last_wrote_time: float = time.time()
        self.__signal_current_no = XSignal()
        self.__signal_current_overload = XSignal()
        self.__signal_shelly_error_occurred = XSignal()
        self.__signal_charged_energy = XSignal()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def main_address(self) -> str:
        return self.__main_address

    @property
    def data_address(self) -> str:
        return f'{self.__main_address}/rpc/EM.GetStatus?id=0'

    @property
    def reset_address(self) -> str:
        return f'{self.__main_address}/rpc/EMData.ResetCounters'

    @property
    def total_energy_address(self) -> str:
        return f'{self.__main_address}/rpc/EMData.GetStatus?id=0'

    @property
    def isAvailable(self) -> bool:
        return self.__isAvailable

    @property
    def charged_energy(self) -> int | float:
        return self.__charged_energy

    @property
    def data(self) -> dict:
        return copy.deepcopy(self.__data)

    @property
    def data_ph0(self) -> dict:
        return copy.deepcopy(self.__data[0])

    @property
    def data_ph1(self) -> dict:
        return copy.deepcopy(self.__data[1])

    @property
    def data_ph2(self) -> dict:
        return copy.deepcopy(self.__data[2])

    @property
    def signal_shelly_error_occurred(self) -> XSignal:
        return self.__signal_shelly_error_occurred

    @property
    def signal_current_no(self) -> XSignal:
        return self.__signal_current_no

    @property
    def signal_current_overload(self) -> XSignal:
        return self.__signal_current_overload

    @property
    def signal_charged_energy(self) -> XSignal:
        return self.__signal_charged_energy

    def set_data(self, data: dict) -> None:
        self.__data = data
        self.__charged_energy = self.__calculate_charged_energy()
        self.__data['charged_energy'] = self.__charged_energy
        # _log.info(f'Shelly data updated: {self.__charged_energy}')
        self.__charged_energy_shelly = self.__data['total_energy']
        self.__parent.parent_obj.data_collector.set_shelly_data(self.id, self.__data)
        # self.__parent.parent_obj.data_collector.set_shelly_charged_energy(self.id, self.__charged_energy)
        self.__isAvailable = self.__data['is_valid']
        if not self.__isAvailable:
            self.signal_shelly_error_occurred.emit(not self.__isAvailable)
            return
        self.signal_charged_energy.emit(self.__charged_energy)

    def __calculate_charged_energy(self) -> int | float:
        """ 
        power: W
        duration: h
        self.__charged_energy: Wh
        """
        if self.__isAvailable:
            duration: float = (time.time() - self.__last_wrote_time) / 3600
            total = 0
            for ph_dict in self.__data.values():
                ph_dict: dict
                if not isinstance(ph_dict, dict):
                    continue
                power = ph_dict.get('power', 0)
                total += (power*duration)
            self.__charged_energy += total
            self.__last_wrote_time = time.time()
        return self.__charged_energy

    def reset(self) -> bool:
        try:
            data = {
                'id': 0  # 通道号
            }
            response0 = requests.post(self.reset_address, json=data, timeout=5)
            response0.raise_for_status()
            self.__last_wrote_time: float = time.time()
            self.__charged_energy = 0
            self.__charged_energy_shelly = 0
            self.__parent.parent_obj.data_collector.set_shelly_charged_energy(self.id, 0)
            _log.info('Shelly 复位成功\nShelly reset successfully')
            return True
        except Exception as e:
            _log.info(f'Shelly 复位失败\nShelly reset failed: {e}')
            return False
