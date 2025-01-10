import traceback

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from threading import Thread, Timer
from sys_basis.XSignal import XSignal
from datetime import datetime
from tools.Inner_Decorators import *
from const.Const_Parameter import *

_info = Log.WEB.info


class ServerWeb(Thread):
    def __init__(self, host='0.0.0.0', port=2311, info_title='Web_Server'):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__app = Flask(__name__, static_folder='static', template_folder='templates')
        self.__app.config['SECRET_KEY'] = 'secret!'
        self.__socketio = SocketIO(self.__app)
        self.__signal_web_server_info = XSignal()
        self.__signal_web_server_recv = XSignal()
        self.__signal_web_server_finished = XSignal()
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        self.__app.add_url_rule('/', 'home', self.__home_route, methods=['GET', 'POST'])
        self.__listening_update()

    @property
    def signal_web_server_info(self):
        return self.__signal_web_server_info

    @property
    def signal_web_server_recv(self):
        return self.__signal_web_server_recv

    @property
    def signal_web_server_finished(self):
        return self.__signal_web_server_finished

    def update_data(self, message: dict):
        if not message:
            return
        self.__socketio.emit('update_data', message)

    def __home_route(self):
        return render_template('HomePage.html')

    def __listening_update(self):
        @self.__socketio.on('update', namespace='/')
        def handle_test(message):
            self.__send_signal_info(f'->>> Web Received> {message}')
            self.signal_web_server_recv.emit(message)

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_web_server_info, error_hint='send_signal_info', log=Log.WEB.info, doShowTitle=True, doPrintInfo=False, args=args)

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
            error_text = f'********************\n<Error - {error_hint}> {traceback.format_exc()}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)

    def run(self):
        self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    web_server = ServerWeb()
    web_server.start()
    web_server.join()
