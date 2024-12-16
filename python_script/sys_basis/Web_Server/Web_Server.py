

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from threading import Thread
from sys_basis.XSignal import XSignal


class WebServer(Thread):
    def __init__(self, host='0.0.0.0', port=2311):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__app = Flask(__name__, static_folder='static', template_folder='templates')
        self.__app.config['SECRET_KEY'] = 'secret!'
        self.__socketio = SocketIO(self.__app)
        self.__signal_web_server_info = XSignal()
        self.__signal_web_server_recv = XSignal()
        self.__signal_web_server_finished = XSignal()
        self.__app.add_url_rule('/', 'home', self.__route)
        self.__app.add_url_rule('/login', 'login', self.__login, methods=['GET', 'POST'])

    @property
    def signal_web_server_info(self):
        return self.__signal_web_server_info

    @property
    def signal_web_server_recv(self):
        return self.__signal_web_server_recv

    @property
    def signal_web_server_finished(self):
        return self.__signal_web_server_finished

    def __login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == 'admin' and password == 'password':
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password, you should input "admin" and "password"')
        return render_template('login.html')

    def update_data(self, message: dict):
        if not message:
            return
        self.__socketio.emit('update_data', message)

    def __route(self):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        if request.method == 'POST':
            json_data = request.get_json()
            self.signal_web_server_recv.emit(json_data)
            return '', 204  # 204 No Content
        return render_template('ChargePointHomePage.html')

    def run(self):
        self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False)


if __name__ == "__main__":
    web_server = WebServer()
    web_server.start()
    web_server.join()
