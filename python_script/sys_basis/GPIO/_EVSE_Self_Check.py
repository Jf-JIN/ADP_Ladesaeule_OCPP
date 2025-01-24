import copy
from threading import Thread

from const.GPIO_Parameter import *
from const.Const_Parameter import *
from sys_basis.XSignal import XSignal
from _Modbus_IO import  ModbusIO
import time

_info = Log.GPIO

class EVSESelfCheck(Thread):
    def __init__(self,id,doUseRCD):
        super().__init__()
        self.__id:int = id
        self.__doUseRCD: bool = doUseRCD
        if doUseRCD:
           self.__set_RCD_test()
        self.__modbus: ModbusIO = ModbusIO(id)
        self.__timeout:int|float = GPIOParams.SELF_CHECK_TIMEOUT
        self.__evse_status_error: set = set()
        self.__running: bool = True
        self.__signal_self_test_error:XSignal= XSignal()



    @property
    def id(self):
        return self.__id

    @property
    def timeout(self):
        return self.__timeout

    @property
    def signal_self_test_error(self):
        return self.__signal_self_test_error

    def __set_RCD_test(self):
        if not self.__doUseRCD:
            return
        with self.__modbus as modbus:
            modbus.enable_RCD(True)

    def set_evse_status_error(self, data:set):
        """
        False 传给EVSE的__enable_charging,True表示可充电,False表示不可充电
        """
        self.__evse_status_error = data
        return True

    def set_selfcheck(self):
        with self.modbus as modbus:
            response = modbus.write_reg1004(bit = 1,flag = 1 )
        return response

    def run(self):
        while self.__running:
            self.set_selfcheck()
            time.sleep(self.__timeout)
            with self.modbus as modbus:
                response = modbus.read_evse_status_fails()
                if self.__doUseRCD:
                    if response:
                        if EVSEFails.RCD_CHECK_ERROR in response:
                            success_clear = modbus.write(address = 1004, value = REG1004.CLEAR_RCD_ERROR)
                            if not success_clear:
                                #这里应该反馈通讯错误？
                                return False
                        else :
                            #如果没有正常显示RCD错误，则认为RCD测试失败
                            self.signal_self_test_error(set('RCD测试失败'))
                            return False
                    else:
                        self.signal_self_test_error(response)





   def stop(self):
        self.__isRunning = False
        self.join()  # 等待线程结束