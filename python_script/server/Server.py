import time

from sys_basis.Ports import *
from sys_basis.XSignal import XSignal
from sys_basis.Manager_Coroutine import ManagerCoroutines


class Server:
    def __init__(self):
        self.__init_signals()
        self.__init_parameters()
        self.__init_threads()
        self.__init_coroutines()
        self.__init_signal_connections()
        self.__thread_web_server.start()
        print(self.__thread_web_server.signal_thread_web_server_info)
        # self.__manager_coroutines.start()

        # self.__coroutine_OCPP_client.start()

        # self.__coroutine_gui_websocket_server.start()

    def __init_signals(self):
        pass

    def __init_signal_connections(self):
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_info.connect(self.__send_info_server_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv.connect(self.__send_info_opt_message)
        # self.__coroutine_OCPP_client.signal_thread_ocpp_client_recv_request
        # self.__coroutine_OCPP_client.signal_thread_ocpp_client_recv_response
        self.__thread_web_server.signal_thread_web_server_info.connect(self.__send_info_server_message)
        self.__thread_web_server.signal_thread_web_server_recv.connect(self.__send_info_server_message)
        # self.__thread_web_server.signal_thread_webs_server_finished
        # self.__coroutine_gui_websocket_server.signal_thread_websocket_client_info.connect(self.__send_info_gui_message)
        # self.__coroutine_gui_websocket_server.signal_thread_websocket_client_recv
        pass

    def __init_parameters(self):
        pass

    def __init_threads(self):
        self.__thread_web_server = PortWebServerOptimizer()

    def __init_coroutines(self):
        self.__coroutine_OCPP_server = PortOCPPWebsocketServer('localhost', 12346, 'CSMS')
        # self.__coroutine_gui_websocket_server = PortWebSocketServer('localhost', 8080)
        # self.__manager_coroutines = ManagerCoroutines(self.__coroutine_OCPP_server.run, self.__coroutine_gui_websocket_server.run)

    def __send_info_server_message(self, message):
        temp_dict = {
            'server_console': message
        }
        print(message)
        if message == 'test':
            self.test(10)
        self.__thread_web_server.send_message(temp_dict)

    def __send_info_opt_message(self, message):
        temp_dict = {
            'opt_console': message
        }
        self.__thread_web_server.send_message(temp_dict)

    # def __send_info_gui_message(self, message):
    #     temp_dict = {
    #         'gui_websocket_console': message
    #     }
    #     self.__thread_web_server.send_message(temp_dict)

    def test(self, num):
        for i in range(num):
            self.__send_info_opt_message(num)
            time.sleep(2)
