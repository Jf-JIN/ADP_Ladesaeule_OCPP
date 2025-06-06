import time
import json

from sys_basis.Ports import *
from sys_basis.Manager_Coroutine import ManagerCoroutines
from sys_basis.Optimize.Optimizer import Optimizer
from const.Opt_Parameter import OptParams
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from const.Charge_Point_Parameters import *
from const.Const_Parameter import *
_debug = Log.CSMS.debug
_info = Log.CSMS.info
_error = Log.CSMS.error
_warning = Log.CSMS.warning


class Server:
    def __init__(self):
        self.__init_signals()
        self.__init_parameters()
        self.__init_threads()
        self.__init_coroutines()
        self.__init_signal_connections()
        self.__thread_web_server.start()
        time.sleep(1)
        self.__manager_coroutines.start()

    def __init_signals(self):
        pass

    def __init_signal_connections(self):
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_info.connect(self.__send_web_ocpp_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv.connect(self.__send_web_ocpp_message)
        # self.__coroutine_OCPP_server.signal_thread_ocpp_server_normal_message.connect(self.__send_info_ocpp_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_request.connect(self.__handle_request_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_response.connect(self.__handle_response_message)
        self.__coroutine_OCPP_server.signal_thread_ocpp_server_recv_response_result.connect(self.__handle_response_result_message)
        # self.__thread_web_server.signal_thread_web_server_info.connect(self.__send_info_web_message)
        self.__thread_web_server.signal_thread_web_server_recv.connect(self.__receive_web_paraments)
        # LoggerGroup.signal_all_color.connect(self.__send_web_console_message)

    def __init_parameters(self):
        self._max_grid_power = OptParams.MAX_GRID_POWER
        self._charging_interval = OptParams.CHARGING_INTERVAL  # minute
        self._eprices = OptParams.EPRICES
        self._send_request_list = []
        self._isopt = False
        self._num_retry_max = OptParams.NUM_RETRY_MAX
        self._num_retry = 0

    def __init_threads(self):
        self.__thread_web_server = PortWebServerOptimizer()

    def __init_coroutines(self):
        self.__coroutine_OCPP_server = PortOCPPWebsocketServer(
            '0.0.0.0',
            80,
            'CSMS',
            recv_timeout_s=CP_Params.RECEIVE_TIMEOUT,
            ocpp_response_timeout_s=CP_Params.RESPONSE_TIMEOUT,
            ping_interval_s=CP_Params.PING_INTERVAL,
            ping_timeout_s=CP_Params.PING_TIMEOUT
        )
        self.__manager_coroutines = ManagerCoroutines(self.__coroutine_OCPP_server)

    def __receive_web_paraments(self, message):
        """
        处理网页数据
        """
        if 'max_grid_power' in message:
            self._max_grid_power = int(message['max_grid_power'])
            self.__thread_web_server.send_console_message({'web_console': 'max_grid_power updated to ' + str(self._max_grid_power) + '\n'})
        if 'charging_interval' in message:
            self._charging_interval = float(message['charging_interval'])
            self.__thread_web_server.send_console_message({'web_console': 'charging_interval updated to ' + str(self._charging_interval) + '\n'})
        if 'eprices' in message:
            self._eprices = message['eprices']
            self.__thread_web_server.send_console_message({'web_console': 'eprices updated' + '\n'})

    def __send_web_console_message(self, message):
        """
        处理网页数据
        """
        temp_dict = {
            'web_console': message
        }
        self.__thread_web_server.send_console_message(temp_dict)

    def __send_web_ocpp_message(self, message):
        """
        处理OCPP消息数据
        """
        temp_dict = {
            'opt_console': message
        }
        self.__thread_web_server.send_console_message(temp_dict)
        if "--<Client_Connected>" in message:
            self.__thread_web_server.send_connection_status({'connection_status': 1, 'ip': message.split("--<Client_Connected> ")[1]})
        if "--<Connection_Closed>" in message:
            self.__thread_web_server.send_connection_status({'connection_status': 0, 'ip': None})

    def __handle_request_message(self, message):
        """
        处理请求信息
        """
        if message['action'] == Action.NotifyEVChargingNeeds:
            self.__handle_notify_ev_charging_needs(message)

    def __handle_notify_ev_charging_needs(self, message):
        """
        处理通知EV充电需求
        """
        self.__thread_web_server.send_charging_needs({
            "evseId": message['data']['evseId'],
            "departureTime": message['data']['chargingNeeds']['departureTime'],
            "energyAmount": message['data']['chargingNeeds']['acChargingParameters']['energyAmount'],
            "evMaxVoltage": message['data']['chargingNeeds']['acChargingParameters']['evMaxVoltage'],
            "evMaxCurrent": message['data']['chargingNeeds']['acChargingParameters']['evMaxCurrent'],
            "evMinCurrent": message['data']['chargingNeeds']['acChargingParameters']['evMinCurrent'],
            "mod": message['data']['customData']['mode']
        })
        opt = Optimizer(
            message['data']['chargingNeeds'],
            self._eprices,
            OptParams.HIS_USAGE,
            self._max_grid_power,
            self._charging_interval,
            message['data']['customData']['mode']
        )
        self._isopt = opt.IsOpt()
        self.__thread_web_server.send_results({
            "results": 1 if self._isopt else 0,
            "img_charging": opt.get_img_charging(),
            "img_comparison": opt.get_img_comparison()})
        # self.__coroutine_OCPP_server.send_normal_message(str({
        #     "opt_img": {
        #         message['data']['evseId']: {
        #             "results": 1 if self._isopt else 0,
        #             "img_charging": opt.get_img_charging(),
        #             "img_comparison": opt.get_img_comparison(),
        #         }
        #     }
        # }))
        self.__coroutine_OCPP_server.send_normal_message(str(json.dumps({
            "opt_result": {
                "opt_img": opt.get_img_charging(),
                "result": 1 if self._isopt else 0,
            }
        })))
        _debug(self._isopt)
        if self._isopt:
            temp_request = GenSetChargingProfileRequest.generate(
                message['data']['evseId'],
                GenSetChargingProfileRequest.get_charging_profile(
                    1,
                    1,
                    ChargingProfilePurposeType.tx_profile,
                    ChargingProfileKindType.absolute,
                    [opt.get_charging_schedule()]
                )
            )
            self._send_request_list.append({
                'action': Action.SetChargingProfile,
                'data': temp_request
            })
            # _info("---------------优化结果加入队列---------------")
            # _info(self._send_request_list)
            self.__coroutine_OCPP_server.send_response_message(
                Action.NotifyEVChargingNeeds,
                GenNotifyEVChargingNeedsResponse.generate(status='Accepted'),
                message['send_time'],
                message['message_id']
            )
            # self.__coroutine_OCPP_server.send_request_message(temp_request)
        else:
            _info("---------------send rejection message---------------")
            self.__coroutine_OCPP_server.send_normal_message('Optimization failed')
            self.__coroutine_OCPP_server.send_response_message(
                Action.NotifyEVChargingNeeds,
                GenNotifyEVChargingNeedsResponse.generate(status='Rejected'),
                message['send_time'],
                message['message_id']
            )

    def __handle_response_message(self, message):
        """
        处理响应信息
        """
        # _info("receive response message:", message, "\n", self._send_request_list)
        if len(self._send_request_list) > 0 and message['action'] == self._send_request_list[-1]['action']:
            if self._isopt:
                if message['result'] == CP_Params.RESPONSE_RESULT.SUCCESS:
                    _info("-------------send request success-------------")
                    self._send_request_list.pop(-1)
                    self._num_retry = 0
                elif message['result'] == CP_Params.RESPONSE_RESULT.ERROR:
                    _info("-------------send request error-------------")
                    self._send_request_list.pop(-1)
                    self._num_retry = 0
                elif message['result'] == CP_Params.RESPONSE_RESULT.TIMEOUT:
                    _info("-------------send request timeout-------------")
                    if self._num_retry < self._num_retry_max:
                        self.__coroutine_OCPP_server.send_request_message(self._send_request_list[-1]['data'])
                        self._num_retry += 1
        # pass

    def __handle_response_result_message(self, message):
        """
        处理响应结果信息
        """
        # _info("receive response result message:", message, "\n", self._send_request_list)
        if message['action'] == Action.NotifyEVChargingNeeds:
            if self._isopt:
                if message['result'] == CP_Params.RESPONSE_RESULT.SUCCESS:
                    _info("-------------notify EV charging needs response success-------------")
                    self.__coroutine_OCPP_server.send_request_message(self._send_request_list[-1]['data'])
                else:
                    _info("-------------notify EV charging needs response failed-------------")
                    self._send_request_list.pop(-1)
        # pass
