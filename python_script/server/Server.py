
from sys_basis.Ports import *
from sys_basis.XSignal import XSignal
from sys_basis.Manager_Coroutine import ManagerCoroutines
from sys_basis.Optimize.Optimizer import Optimizer
from const.Opt_Parameter import OptParams
from ocpp.v201.enums import *
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from const.Charge_Point_Parameters import *


class Server:
    def __init__(self):
        self._max_grid_power = 16000
        self._send_request_list = []
        self.__init_signals()
        self.__init_parameters()
        self.__init_threads()
        self.__init_coroutines()
        self.__init_signal_connections()
        self.__thread_web_server.start()
        # print(self.__thread_web_server.signal_thread_web_server_info)
        self.__manager_coroutines.start()

        # self.__coroutine_OCPP_server.start()

        # self.__coroutine_gui_websocket_server.start()

    def __init_signals(self):
        pass

    def __init_signal_connections(self):
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_info.connect(self.__send_info_opt_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv.connect(self.__send_info_opt_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_normal_message.connect(self.__send_info_opt_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_request.connect(self.__handle_request_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_response.connect(self.__handle_response_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_response_result.connect(self.__handle_response_result_message)
        # self.__thread_web_server.signal_thread_web_server_info.connect(self.__send_info_web_message)
        self.__thread_web_server.signal_thread_web_server_recv.connect(self.__send_info_web_message)
        # self.__thread_web_server.signal_thread_webs_server_finished
        # self.__coroutine_gui_websocket_server.signal_thread_websocket_client_info.connect(self.__send_info_gui_message)
        # self.__coroutine_gui_websocket_server.signal_thread_websocket_client_recv
        pass

    def __init_parameters(self):
        pass

    def __init_threads(self):
        self.__thread_web_server = PortWebServerOptimizer()

    def __init_coroutines(self):
        self.__coroutine_OCPP_server = PortOCPPWebsocketServer('0.0.0.0', 80, 'CSMS')
        # self.__coroutine_gui_websocket_server = PortWebSocketServer('localhost', 8080)
        self.__manager_coroutines = ManagerCoroutines(self.__coroutine_OCPP_server.run)

    def __send_info_web_message(self, message):
        temp_dict = {
            'web_console': message
        }
        # print(message)
        if 'max_grid_power' in message:
            self._max_grid_power = message['max_grid_power']
            self.__thread_web_server.send_message({'web_console': 'max_grid_power updated to ' + str(self._max_grid_power)})
        else:
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

    def __handle_request_message(self, message):
        if message['action'] == Action.NotifyEVChargingNeeds:
            self.__handle_notify_ev_charging_needs(message)

    def __handle_notify_ev_charging_needs(self, message):
        opt = Optimizer(
            message['data']['chargingNeeds'],
            OptParams.EPRICES,
            OptParams.HIS_USAGE,
            self._max_grid_power,
            15,
            message['data']['customData']['mod']
        )
        if not opt.IsOpt():
            self.__coroutine_OCPP_server.send_response_message(
                Action.NotifyEVChargingNeeds,
                notify_ev_charging_needs_response.generate(status='Accepted'),
                message['send_time']
            )
            temp_request = set_charging_profile_request.generate(
                    message['data']['evseId'],
                    set_charging_profile_request.get_charging_profile(
                        1,
                        1,
                        ChargingProfilePurposeType.tx_profile,
                        ChargingProfileKindType.absolute,
                        [opt.get_charging_schedule()]
                    )
                )
            self._send_request_list.append({
                'action': 'NotifyEVChargingNeeds',
                'data': temp_request
            })
            # print(self._send_request_list)
            self.__coroutine_OCPP_server.send_request_message(temp_request)
        else:
            self.__coroutine_OCPP_server.send_response_message(
                Action.NotifyEVChargingNeeds,
                notify_ev_charging_needs_response.generate(status='Rejected'),
                message['send_time']
            )

    def __handle_response_message(self, message):
        pass

    def __handle_response_result_message(self, message):
        # if len(self._send_request_list) > 0 and message['action'] == self._send_request_list[-1]['action']:
        #     if message['status'] == CP_Params.RESPONSE_RESULT.SUCCESS:
        #         self._send_request_list.pop(-1)
        #         print("芜湖! ! ! ! ! ! ! ! ")
        #     if message['status'] == CP_Params.RESPONSE_RESULT.TIMEOUT:
        #         self.__coroutine_OCPP_server.send_request_message(self._send_request_list[-1]['data'])
        pass
