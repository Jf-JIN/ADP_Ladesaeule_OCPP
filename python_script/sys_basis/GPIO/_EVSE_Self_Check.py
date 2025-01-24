from threading import Thread

from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from _Modbus_IO import  ModbusIO
import time

_info = Log.GPIO

class EVSESelfCheck(Thread):
    def __init__(self,id:int,doUseRCD:bool=False)->None:
        super().__init__()
        self.__id:int = id
        self.__timeout:int|float = GPIOParams.SELF_CHECK_TIMEOUT
        self.__signal_self_test_error:XSignal= XSignal()
        self.__running:bool = True
        self.__modbus:ModbusIO = ModbusIO(id)
        self.__doUseRCD:bool = doUseRCD

    @property
    def id(self):
        return self.__id

    @property
    def timeout(self):
        return self.__timeout

    @property
    def signal_self_test_error(self,error_index):
        """
        False 传给EVSE的__enable_charging,True表示可充电,False表示不可充电
        """
        return self.__signal_self_test_error.emit(error_index)


    def run(self, ):
        while self.__running:
            with self.__modbus as modbus:
                selftest_successful_start = modbus.run_selftest_and_RCD_test_procedure()
                if selftest_successful_start:
                    time.sleep(self.__timeout)
                    response = modbus.read_evse_status_fails()
                    if self.__doUseRCD:
                        if response:
                            if 'RCD Check Error' in response:
                                success_clear = modbus.write(address = EVSERegAddress.TURN_OFF_SELFTEST_OPERATION, value = BitsFlag.REG1004.CLEAR_RCD_ERROR)
                                if not success_clear:
                                    #这里应该反馈通讯错误？
                                    return False
                            else :
                                #如果没有正常显示RCD错误，则认为RCD测试失败
                                self.signal_self_test_error(set('RCD测试失败'))
                        else:
                            self.signal_self_test_error(response)





   def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束