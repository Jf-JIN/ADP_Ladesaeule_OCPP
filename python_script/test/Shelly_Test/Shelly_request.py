
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DToolslib import *
from Widget_Controle_TextBrowser import *


import requests
import os
import datetime
import sys


_log = Logger(__name__, os.path.dirname(__file__))

# main_url = "http://shellypro3em-2cbcbbb2e0b8.local"
# main_url = "http://127.0.0.1:6666"
main_url = "http://192.168.124.9:6666"
# main_url = "http://192.168.1.103:6666"


total_energy_url = main_url + '/rpc/EMData.GetStatus?id=0'
reset_url = main_url+"/rpc/EMData.ResetCounters"


def req():
    try:
        response_energy: requests.Response = requests.get(total_energy_url, timeout=2)
        response_energy.raise_for_status()
        data_energy: dict = response_energy.json()
        _log.info(data_energy)
        return data_energy
    except requests.exceptions.RequestException as e:
        _log.exception(e)
        return {'error': e}


def clear():
    # try:
    #     response_reset = requests.Response = requests.get(reset_url, timeout=2)
    #     response_reset.raise_for_status()
    #     _log.info('已重置\n'+response_reset)
    #     return response_reset.json()
    # except requests.exceptions.RequestException as e:
    #     _log.exception(e)
    #     return {'error': e}

    try:
        # 发送 POST 请求
        # reset_token = 'rpc/EMData.ResetCounters?id=0'
        reset_token = 'rpc/EMData.ResetCounters'
        data = {
            "id": 0  # 通道号
        }
        response0 = requests.post(reset_url, json=data, timeout=5)
        response0.raise_for_status()
        _log.info("Shelly 复位成功\nShelly reset successfully")
        return response0.json()
    except Exception as e:
        _log.info(f"Shelly 复位失败\nShelly reset failed: {e}")
        return {'error': e}


class EXE(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Shelly")
        self.resize(800, 600)
        self.w = QWidget(self)
        self.setCentralWidget(self.w)
        self.pb_clear = QPushButton("Clear", self)
        self.pb_clear.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pb_clear.clicked.connect(self.reset_req)
        self.textbrowser = ControlTextBrowser(font_size=30)
        self.textbrowser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self.w)
        layout.addWidget(self.textbrowser)
        layout.addWidget(self.pb_clear)
        layout.setStretch(0, 100)
        layout.setStretch(1, 10)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.show()

    def update_data(self):
        data = req()
        self.show_data(data)

    def reset_req(self):
        data = clear()
        self.show_data(data)

    def show_data(self, data: dict) -> None:
        self.textbrowser.append_text(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'+str(data)+'\n')


_log.info('dddd'*10000)
_log.info('dddd'*10000)
_log.info('dddd'*10000)
_log.info('dddd'*10000)
_log.info('dddd'*10000)

app = QApplication(sys.argv)
exe = EXE()
sys.exit(app.exec_())
