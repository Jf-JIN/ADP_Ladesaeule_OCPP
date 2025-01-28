# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_socketio import SocketIO
import random
import threading


class ServerWeb:
    def __init__(self, host='0.0.0.0', port=6666, async_mode='threading'):
        self.__host: str = host
        self.__port: int = port
        self.__app = Flask(__name__)
        self.__app.config['SECRET_KEY'] = 'secret!'
        self.__socketio = SocketIO(self.__app)
        self.__period = 1
        self.__total0 = 0
        self.__total1 = 0
        self.__total2 = 0
        self.__power0 = 0
        self.__power1 = 0
        self.__power2 = 0
        self.__timer0 = threading.Timer(self.__period, self.__total_update0)
        self.__timer1 = threading.Timer(self.__period, self.__total_update1)
        self.__timer2 = threading.Timer(self.__period, self.__total_update2)
        self.__timer0.start()
        self.__timer1.start()
        self.__timer2.start()

        # 添加路由，访问不同的 URL 时返回不同的 JSON 数据
        self.__app.add_url_rule('/emeter/0', '0', self.__phase0, methods=['GET'])
        self.__app.add_url_rule('/emeter/1', '1', self.__phase1, methods=['GET'])
        self.__app.add_url_rule('/emeter/2', '2', self.__phase2, methods=['GET'])
        self.__app.add_url_rule('/emeter/0/reset_totals', 'reset_totals0', self.clear0, methods=['GET', 'POST'])
        self.__app.add_url_rule('/emeter/1/reset_totals', 'reset_totals1', self.clear1, methods=['GET', 'POST'])
        self.__app.add_url_rule('/emeter/2/reset_totals', 'reset_totals2', self.clear2, methods=['GET', 'POST'])
        self.__app.add_url_rule('/reset_totals', 'reset_totals', self.clear, methods=['GET', 'POST'])

    def __get_value(self):
        return (
            random.uniform(15, 25),
            random.uniform(210, 230),
            random.uniform(0.87, 0.98)
        )

    def __phase0(self):
        """返回固定的 JSON 数据"""
        amps, voltage, factor = self.__get_value()
        self.__power0 = amps*voltage*factor
        temp_dict = {
            'power': self.__power0,
            'pf': factor,
            'current': amps,
            'voltage': voltage,
            'is_valid': True,
            'total': self.__total0,
            'total_returned': 0
        }
        return jsonify(temp_dict)

    def __phase1(self):
        """返回第二个设备的数据"""
        amps, voltage, factor = self.__get_value()
        self.__power1 = amps*voltage*factor
        print('ddddddddddd', self.__power1)
        temp_dict = {
            'power': self.__power1,
            'pf': factor,
            'current': amps,
            'voltage': voltage,
            'is_valid': True,
            'total': self.__total1,
            'total_returned': 0
        }
        return jsonify(temp_dict)

    def __phase2(self):
        """返回第三个设备的数据"""
        amps, voltage, factor = self.__get_value()
        self.__power2 = amps*voltage*factor
        temp_dict = {
            'power': self.__power2,
            'pf': factor,
            'current': amps,
            'voltage': voltage,
            'is_valid': True,
            'total': self.__total2,
            'total_returned': 0
        }
        return jsonify(temp_dict)

    def __total_update0(self):
        self.__total0 += self.__period * self.__power0 / 3600
        self.__timer0 = threading.Timer(self.__period, self.__total_update0)
        self.__timer0.start()

    def __total_update1(self):
        self.__total1 += self.__period * self.__power1 / 3600
        self.__timer1 = threading.Timer(self.__period, self.__total_update1)
        self.__timer1.start()

    def __total_update2(self):
        self.__total2 += self.__period * self.__power2 / 3600
        self.__timer2 = threading.Timer(self.__period, self.__total_update2)
        self.__timer2.start()

    def clear0(self):
        self.__total0 = 0
        return ''

    def clear1(self):
        self.__total1 = 0
        return ''

    def clear2(self):
        self.__total2 = 0
        return ''

    def clear(self):
        self.clear0()
        self.clear1()
        self.clear2()
        return ''

    def run(self):
        self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False)


if __name__ == "__main__":
    web_server = ServerWeb()
    web_server.run()
