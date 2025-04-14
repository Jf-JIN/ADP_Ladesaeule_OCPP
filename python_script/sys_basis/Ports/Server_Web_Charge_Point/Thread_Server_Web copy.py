

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from werkzeug import serving
from socket import AddressFamily
from threading import Thread, Timer
from sys_basis.XSignal import XSignal
from const.Const_Parameter import *
from datetime import datetime
from tools.Inner_Decorators import *
import requests
from DToolslib import *


class ServerWeb(Thread):
    def __init__(self, host='0.0.0.0', port=2311, info_title='Web_Server'):
        super().__init__(name='ServerWeb')
        self.__host: str = host
        self.__port: int = port
        self.__app = Flask(__name__, static_folder='static', template_folder='templates')
        self.__app.config['SECRET_KEY'] = 'secret!'
        # self.__socketio = SocketIO(self.__app)
        self.__socketio = SocketIO()
        self.__socketio.init_app(self.__app)
        self.__signal_web_server_info = XSignal()
        self.__signal_web_server_recv = XSignal()
        self.__signal_web_server_finished = XSignal()
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        self.__app.add_url_rule('/', 'admin', self.__admin_route, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/admin', 'admin', self.__admin_route, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/', 'login', self.__login, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/user', 'user', self.__user_route, methods=['GET', 'POST'])
        self.__start_timer()
        self.__listening_input_data()
        self.__logout()
        self.__ip_local: str = '127.0.0.1' if host == '0.0.0.0' else '[::1]'
        self.__ip_remote: str = serving.get_interface_ip(AddressFamily.AF_INET)
        self.__ip_local_address: str = f'http://{self.__ip_local}:{port}'
        self.__ip_remote_address: str = f'http://{self.__ip_remote}:{port}'
        self.__send_signal_info(f'Web Server started on \n\t- local : {self.__ip_local_address}\n\t- remote: {self.__ip_remote_address}')

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
        if hasattr(self, f'_{self.__class__.__name__}__socketio') and self.__app:
            self.__socketio.emit('update_data', message)

    def __start_timer(self):
        self.__timer = Timer(1.0, self.__send_time)
        self.__timer.name = 'ServerWeb.sendTime'
        self.__timer.start()

    def __send_time(self):
        self.__socketio.emit('current_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.__start_timer()

    def __login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            login_type = request.form.get('login_type')
            if login_type == 'user':
                return redirect(url_for('user'))
            if username == 'admin' and password == 'password':
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                text = """Invalid username or password, you should input 'admin' and 'password' """
                flash(text)
            return redirect(url_for('login'))
        return render_template('login.html')

    def __admin_route(self):
        # if not session.get('logged_in'):
        #     return redirect(url_for('login'))
        return render_template('AdminPage.html')

    def __user_route(self):
        return render_template('UserPage.html')

    def __listening_input_data(self):
        @self.__socketio.on('input_data', namespace='/')
        def handle_input_data(message):
            # self.__send_signal_info(f'->>> Web Received> {message}')
            self.signal_web_server_recv.emit(message)

    def __logout(self):
        @self.__socketio.on('logout', namespace='/')
        def handle_logout():
            session.pop('logged_in', None)
            self.__socketio.emit('redirect_to_login', namespace='/')

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_web_server_info, error_hint='send_signal_info', log=Log.WEB.info, doShowTitle=True, doPrintInfo=False, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
        - signal(XSignal): 信号对象
        - error_hint(str): 错误提示
        - log: 日志器动作
        - doShowTitle(bool): 是否显示标题
        - doPrintInfo(bool): 是否打印信息
        - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
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

    def run(self):
        self.__app.run(host=self.__host, port=self.__port, debug=False, threaded=True)
        # self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False)

    def stop(self):
        request.environ.get('werkzeug.server.shutdown')()
        self._stop_requested = True
        if hasattr(self, f'_{self.__class__.__name__}__timer') and self.__timer:
            self.__timer.cancel()
        # if hasattr(self, f'_{self.__class__.__name__}__socketio') and self.__socketio:
        #     self.__app = None
        #     self.__socketio = SocketIO(None)
            # del self.__socketio
            # del self.__app
        del self


if __name__ == "__main__":
    web_server = ServerWeb()
    web_server.start()
    web_server.join()
