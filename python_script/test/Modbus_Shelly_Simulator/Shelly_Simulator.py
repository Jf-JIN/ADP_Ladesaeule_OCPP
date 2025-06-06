
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from socket import AddressFamily
from werkzeug import serving
import random
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

import os
import signal


class ShellySimulator_Thread(QThread):
    signal_ip_address = pyqtSignal(list)
    signal_ph0 = pyqtSignal(dict)
    signal_ph1 = pyqtSignal(dict)
    signal_ph2 = pyqtSignal(dict)
    signal_start = pyqtSignal(bool)

    def __init__(self, host='0.0.0.0', port=6666):
        super().__init__()
        self.__host: str = host
        self.__port: int = port
        self.__app = Flask(__name__)
        self.__app.config['SECRET_KEY'] = 'secret!'
        self.__socketio = SocketIO(self.__app, async_mode='threading')
        self.__current_target_value = 0
        self.__voltage_target_value = 230
        self.__factor_target_value = 0.90
        self.__current_tolerance = 1
        self.__voltage_tolerance = 10
        self.__factor_tolerance = 0.04
        self.__current_min_value = 0
        self.__current_max_value = 80
        self.__period_ms = 100
        self.__isVaild = True
        self.__isTurnedOn = False
        self.__isPresent = False
        self.__energy_rate = 1
        self.__init_parameters()
        self.__set_value()
        self.__timer = QTimer()
        self.__timer.setInterval(self.__period_ms)
        self.__timer.timeout.connect(self.__set_value)
        self.__timer.start()

        # 添加路由，访问不同的 URL 时返回不同的 JSON 数据
        self.__app.add_url_rule('/rpc/EM.GetStatus', 'em_get_status', self.__phase, methods=['GET', 'POST'])
        self.__app.add_url_rule('/rpc/EMData.GetStatus', 'emdaata_get_status', self.__total_energy, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/emeter/0', '0', self.__phase0, methods=['GET'])
        # self.__app.add_url_rule('/emeter/1', '1', self.__phase1, methods=['GET'])
        # self.__app.add_url_rule('/emeter/2', '2', self.__phase2, methods=['GET'])
        # self.__app.add_url_rule('/emeter/0/reset_totals', 'reset_totals0', self.clear0, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/emeter/1/reset_totals', 'reset_totals1', self.clear1, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/emeter/2/reset_totals', 'reset_totals2', self.clear2, methods=['GET', 'POST'])
        # self.__app.add_url_rule('/rpc/EMData.ResetCounters', 'ResetCounters', self.clear, methods=['GET', 'POST'])
        self.__app.add_url_rule('/rpc/EMData.ResetCounters', 'em_data_resetCounters', self.clear, methods=['GET', 'POST'])
        self.__ip_local: str = '127.0.0.1' if host == '0.0.0.0' else '[::1]'
        self.__ip_remote: str = serving.get_interface_ip(AddressFamily.AF_INET)
        self.__ip_local_address: str = f'{self.__ip_local}:{port}'
        self.__ip_remote_address: str = f'{self.__ip_remote}:{port}'

    def __init_parameters(self):
        self.__current_p0 = 0
        self.__current_p1 = 0
        self.__current_p2 = 0
        self.__voltage_p0 = 0
        self.__voltage_p1 = 0
        self.__voltage_p2 = 0
        self.__factor_p0 = 0
        self.__factor_p1 = 0
        self.__factor_p2 = 0
        self.__power_p0 = 0
        self.__power_p1 = 0
        self.__power_p2 = 0
        self.__total_power_p0 = 0
        self.__total_power_p1 = 0
        self.__total_power_p2 = 0
        self.__total_power_p0 = 0
        self.__total_power_p1 = 0
        self.__total_power_p2 = 0

    def __set_value(self):
        if self.__isTurnedOn and self.__isVaild and self.__current_target_value > 0 and self.__isPresent:
            # self.__current_p0 = min(self.__current_max_value, max(self.__current_min_value, random.uniform(
            #     self.__current_target_value-self.__current_tolerance,
            #     self.__current_target_value+self.__current_tolerance
            # )))
            # self.__current_p1 = min(self.__current_max_value, max(self.__current_min_value, random.uniform(
            #     self.__current_target_value-self.__current_tolerance,
            #     self.__current_target_value+self.__current_tolerance
            # )))
            # self.__current_p2 = min(self.__current_max_value, max(self.__current_min_value, random.uniform(
            #     self.__current_target_value-self.__current_tolerance,
            #     self.__current_target_value+self.__current_tolerance
            # )))
            self.__current_p0 = random.uniform(
                self.__current_target_value-self.__current_tolerance,
                self.__current_target_value+self.__current_tolerance
            )
            self.__current_p1 = random.uniform(
                self.__current_target_value-self.__current_tolerance,
                self.__current_target_value+self.__current_tolerance
            )
            self.__current_p2 = random.uniform(
                self.__current_target_value-self.__current_tolerance,
                self.__current_target_value+self.__current_tolerance
            )
            self.__voltage_p0 = max(0, random.uniform(
                self.__voltage_target_value-self.__voltage_tolerance,
                self.__voltage_target_value+self.__voltage_tolerance
            ))
            self.__voltage_p1 = max(0, random.uniform(
                self.__voltage_target_value-self.__voltage_tolerance,
                self.__voltage_target_value+self.__voltage_tolerance
            ))
            self.__voltage_p2 = max(0, random.uniform(
                self.__voltage_target_value-self.__voltage_tolerance,
                self.__voltage_target_value+self.__voltage_tolerance
            ))
            self.__factor_p0 = max(0, random.uniform(
                self.__factor_target_value-self.__factor_tolerance,
                self.__factor_target_value+self.__factor_tolerance
            ))
            self.__factor_p1 = max(0, random.uniform(
                self.__factor_target_value-self.__factor_tolerance,
                self.__factor_target_value+self.__factor_tolerance
            ))
            self.__factor_p2 = max(0, random.uniform(
                self.__factor_target_value-self.__factor_tolerance,
                self.__factor_target_value+self.__factor_tolerance
            ))
            self.signal_start.emit(True)
        else:
            self.__current_p0 = 0
            self.__current_p1 = 0
            self.__current_p2 = 0
            self.__voltage_p0 = 0
            self.__voltage_p1 = 0
            self.__voltage_p2 = 0
            self.__factor_p0 = 0
            self.__factor_p1 = 0
            self.__factor_p2 = 0
            self.signal_start.emit(False)
        self.__power_p0 = self.__current_p0 * self.__voltage_p0 * self.__factor_p0
        self.__power_p1 = self.__current_p1 * self.__voltage_p1 * self.__factor_p1
        self.__power_p2 = self.__current_p2 * self.__voltage_p2 * self.__factor_p2
        self.__power_ori_p0 = self.__current_p0 * self.__voltage_p0
        self.__power_ori_p1 = self.__current_p1 * self.__voltage_p1
        self.__power_ori_p2 = self.__current_p2 * self.__voltage_p2
        self.__total_power_p0 += (self.__period_ms / 1000) / 3600 * self.__power_p0 * self.__energy_rate
        self.__total_power_p1 += (self.__period_ms / 1000) / 3600 * self.__power_p1 * self.__energy_rate
        self.__total_power_p2 += (self.__period_ms / 1000) / 3600 * self.__power_p2 * self.__energy_rate
        self.__total_power = self.__total_power_p0 + self.__total_power_p1 + self.__total_power_p2
        self.__ph_dict = {
            "id": 0,
            "a_current": self.__current_p0,
            "a_voltage": self.__voltage_p0,
            "a_act_power": self.__power_p0,
            "a_aprt_power": self.__power_ori_p0,
            "a_pf": self.__factor_p0,
            "a_freq": 50.0,

            "b_current": self.__current_p1,
            "b_voltage": self.__voltage_p1,
            "b_act_power": self.__power_p1,
            "b_aprt_power": self.__power_ori_p1,
            "b_pf": self.__factor_p1,
            "b_freq": 50.0,

            "c_current": self.__current_p2,
            "c_voltage": self.__voltage_p2,
            "c_act_power": self.__power_p2,
            "c_aprt_power": self.__power_ori_p2,
            "c_pf": self.__factor_p2,
            "c_freq": 50.0,

            "n_current": None,
            "total_current": self.__current_p0 + self.__current_p1 + self.__current_p2,
            "total_act_power": self.__total_power,
            "total_aprt_power": self.__power_ori_p0 + self.__power_ori_p1 + self.__power_ori_p2,
            "user_calibrated_phase": []
        }
        self.__total_energy_dict = {
            'a_total_act_energy': self.__total_power_p0,
            'a_total_act_ret_energy': 0.0,
            'b_total_act_energy': self.__total_power_p1,
            'b_total_act_ret_energy': 0.0,
            'c_total_act_energy': self.__total_power_p2,
            'c_total_act_ret_energy': 0.0,
            'id': 0,
            'total_act': self.__total_power,
            'total_act_ret': 0.0
        }
        self.__ph0_dict = {
            'power': self.__power_p0,
            'pf': self.__factor_p0,
            'current': self.__current_p0,
            'voltage': self.__voltage_p0,
            'is_valid': self.__isVaild,
            'total': self.__total_power_p0,
            'total_returned': 0
        }
        self.__ph1_dict = {
            'power': self.__power_p1,
            'pf': self.__factor_p1,
            'current': self.__current_p1,
            'voltage': self.__voltage_p1,
            'is_valid':  self.__isVaild,
            'total': self.__total_power_p1,
            'total_returned': 0
        }
        self.__ph2_dict = {
            'power': self.__power_p2,
            'pf': self.__factor_p2,
            'current': self.__current_p2,
            'voltage': self.__voltage_p2,
            'is_valid':  self.__isVaild,
            'total': self.__total_power_p2,
            'total_returned': 0
        }
        self.signal_ph0.emit(self.__ph0_dict)
        self.signal_ph1.emit(self.__ph1_dict)
        self.signal_ph2.emit(self.__ph2_dict)

    def set_inVaild(self):
        self.__isVaild = not self.__isVaild

    def handle_thread_data(self, data_dict: dict):
        self.__current_target_value = data_dict.get('1000', 0)
        self.__current_max_value = data_dict.get('1003', 6)
        self.__current_min_value = data_dict.get('2002', 5)
        self.__isPresent = 1 < data_dict.get('1002', 1) < 5
        self.__isTurnedOn = not data_dict.get('1004', 0) & 1 << 0
        self.__voltage_target_value = data_dict.get('max_voltage', 230)

    def set_current_target_value(self, target):
        self.__current_target_value = target

    def set_current_max_value(self, max_value):
        self.__current_max_value = max_value

    def set_current_min_value(self, min_value):
        self.__current_min_value = min_value

    def set_energy_rate(self, energy_rate):
        self.__energy_rate = energy_rate

    def __phase0(self):
        return jsonify(self.__ph0_dict)

    def __phase1(self):
        return jsonify(self.__ph1_dict)

    def __phase2(self):
        return jsonify(self.__ph2_dict)

    def __phase(self):
        id_param = request.args.get('id')  # 会读取 ?id=0 中的 id
        print(f"Received id: {id_param}")
        return jsonify(self.__ph_dict)

    def __total_energy(self):
        id_param = request.args.get('id')  # 会读取 ?id=0 中的 id
        print(f"Received id: {id_param} total_energy")
        return jsonify(self.__total_energy_dict)

    def clear0(self):
        self.__total_power_p0 = 0
        return ''

    def clear1(self):
        self.__total_power_p1 = 0
        return ''

    def clear2(self):
        self.__total_power_p2 = 0
        return ''

    def clear_total_energy(self):
        self.__total_power_p0 = 0
        self.__total_power_p1 = 0
        self.__total_power_p2 = 0
        self.__total_power = 0
        return ''

    def clear(self):
        self.clear0()
        self.clear1()
        self.clear2()
        self.clear_total_energy()
        return ''

    def run(self):
        self.signal_ip_address.emit([self.__ip_local_address, self.__ip_remote_address])
        self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False, use_reloader=False)

    def stop(self):
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    web_server = ShellySimulator_Thread()
    web_server.run()
