

from threading import Thread
from sys_basis.XSignal import XSignal
from sys_basis.Ports.Server_Web_Optimizer import ServerWeb
from const.Const_Parameter import *

_info = Log.WEB.info


class PortWebServerOptimizer(Thread):
    def __init__(self, host='0.0.0.0', port=1132, info_title='Web_Server_Port'):
        super().__init__(name='PortWebServerOptimizer')
        self.__signal_thread_web_server_info = XSignal()
        self.__signal_thread_web_server_recv = XSignal()
        self.__signal_thread_webs_server_finished = XSignal()

        self.__web_server = ServerWeb(host, port)
        self.__web_server.signal_web_server_info.connect(self.signal_thread_web_server_info.emit)
        self.__web_server.signal_web_server_recv.connect(self.signal_thread_web_server_recv.emit)
        self.__web_server.signal_web_server_finished.connect(self.signal_thread_webs_server_finished.emit)

        self.__isRunning = True
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    @property
    def signal_thread_web_server_info(self) -> XSignal:
        return self.__signal_thread_web_server_info

    @property
    def signal_thread_web_server_recv(self) -> XSignal:
        return self.__signal_thread_web_server_recv

    @property
    def signal_thread_webs_server_finished(self) -> XSignal:
        return self.__signal_thread_webs_server_finished

    def send_console_message(self, message: dict):
        self.__web_server.update_console_data(message)

    def send_charging_needs(self, message: dict):
        self.__web_server.update_charging_needs(message)

    def send_connection_status(self, message: dict):
        self.__web_server.update_connection_status(message)

    def send_results(self, message: dict):
        self.__web_server.update_results(message)

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.__signal_thread_web_server_info, error_hint='send_signal_info', log=Log.WEB.info, doShowTitle=True, doPrintInfo=False, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=None) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
        - signal(XSignal): 信号对象
        - error_hint(str): 错误提示
        - log: 日志器动作
        - doShowTitle(bool): 是否显示标题
        - doPrintInfo(bool): 是否打印信息
        - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        if args is None:
            args = []
        try:
            temp = ''.join([str(*args)]) + '\n'
            if self.__info_title and doShowTitle:
                temp = f'< {self.__info_title} >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)

    def stop(self) -> None:
        """
        终止线程

        `__isRunning` 将设置为 `False`
        """
        self.__isRunning = False
        self.__signal_thread_webs_server_finished.emit()

    def run(self):
        self.__web_server.start()
