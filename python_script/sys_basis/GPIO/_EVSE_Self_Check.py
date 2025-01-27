
from threading import Thread

from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from _Modbus_IO import ModbusIO
import time

_info = Log.EVSE.info
_error = Log.EVSE.error


class EVSESelfCheck(Thread):
    isChecking = False

    def __init__(self, id: int, doUseRCD: bool = False):
        super().__init__()
        self.__id: int = id
        self.__doUseRCD: bool = doUseRCD
        if doUseRCD:
            self.__set_RCD_test()
        self.__modbus: ModbusIO = ModbusIO(id)
        self.__timeout: int | float = GPIOParams.SELF_CHECK_TIMEOUT
        self.__rw_error: set = set()
        self.__isRunning: bool = True
        self.__isNoError: bool = False
        self.__signal_self_test_error: XSignal = XSignal()
        self.__signal_test_finished_result: XSignal = XSignal()

    @property
    def id(self):
        return self.__id

    @property
    def timeout(self):
        return self.__timeout

    @property
    def isRunning(self):
        return self.__isRunning

    @property
    def signal_self_test_error(self):
        return self.__signal_self_test_error

    @property
    def signal_test_finished_result(self):
        return self.__signal_test_finished_result

    def __set_RCD_test(self):
        if not self.__doUseRCD:
            return
        with self.__modbus as modbus:
            modbus.enable_RCD(True)

    def __exit_self_test(self):
        if self.__id in self.__modbus.__class__.isSelfChecking:
            self.__modbus.__class__.isSelfChecking.remove(self.__id)
        self.__isRunning = False
        self.__class__.isChecking = False
        self.__signal_test_finished_result.emit(self.__isNoError)

    def run(self):
        if self.__timeout <= 30:
            _error(f'EVSE {self.__id} timeout must be greater than 30s')
            return
        if self.__class__.isChecking:
            _error(f'EVSE {self.__id} is self checking. Cannot start again.')
            return
        self.__class__.isChecking = True

        while self.__isRunning:
            with self.__modbus as modbus:
                res = modbus.run_selftest_and_RCD_test_procedure()
                if not res:
                    self.__rw_error.add(EVSEErrorInfo.READ_ERROR)
                    self.__signal_self_test_error.emit(self.__rw_error)
                    self.__exit_self_test()
                    return  # 读写错误, 直接结束自检

                time.sleep(self.__timeout)

                response = modbus.read_evse_status_fails()
                if not response:
                    self.__rw_error.add(EVSEErrorInfo.READ_ERROR)
                    self.__signal_self_test_error.emit(self.__rw_error)
                    self.__exit_self_test()
                    return  # 读写错误, 直接结束自检

                if self.__doUseRCD:
                    if EVSEErrorInfo.RCD_CHECK_ERROR in response:
                        response.remove(EVSEErrorInfo.RCD_CHECK_ERROR)
                        success_clear = modbus.clear_RCD()
                        if not success_clear:
                            self.__rw_error.add(EVSEErrorInfo.WRITE_ERROR)
                            self.__signal_self_test_error.emit(self.__rw_error)
                            self.__exit_self_test()
                            return
                        self.__isNoError = True
                    else:
                        # 如果没有正常显示RCD错误, 则认为RCD测试失败
                        response.add(EVSEErrorInfo.RCD_CHECK_FAILED)
                else:
                    self.__isNoError = True

                self.signal_self_test_error.emit(response)
                self.__exit_self_test()

    def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束
