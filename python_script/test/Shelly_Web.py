from flask import Flask, jsonify
from flask_socketio import SocketIO


class ServerWeb:
    def __init__(self, host='0.0.0.0', port=6666):
        self.__host: str = host
        self.__port: int = port
        self.__app = Flask(__name__)
        self.__app.config['SECRET_KEY'] = 'secret!'
        self.__socketio = SocketIO(self.__app)

        # 添加路由，访问不同的 URL 时返回不同的 JSON 数据
        self.__app.add_url_rule('/emeter/0', '0', self.__phase0, methods=['GET'])
        self.__app.add_url_rule('/emeter/1', '1', self.__phase1, methods=['GET'])
        self.__app.add_url_rule('/emeter/2', '2', self.__phase2, methods=['GET'])

    def __phase0(self):
        """返回固定的 JSON 数据"""
        temp_dict = {
            'power': 4400,
            'pf': 0.98,
            'current': 20,
            'voltage': 220,
            'is_valid': True,
            'total': 100,
            'total_returned': 5
        }
        return jsonify(temp_dict)

    def __phase1(self):
        """返回第二个设备的数据"""
        temp_dict = {
            'power': 3300,
            'pf': 0.95,
            'current': 15,
            'voltage': 220,
            'is_valid': True,
            'total': 150,
            'total_returned': 8
        }
        return jsonify(temp_dict)

    def __phase2(self):
        """返回第三个设备的数据"""
        temp_dict = {
            'power': 2200,
            'pf': 0.90,
            'current': 10,
            'voltage': 220,
            'is_valid': True,
            'total': 200,
            'total_returned': 12
        }
        return jsonify(temp_dict)

    def run(self):
        self.__socketio.run(self.__app, host=self.__host, port=self.__port, debug=False)


if __name__ == "__main__":
    web_server = ServerWeb()
    web_server.run()
