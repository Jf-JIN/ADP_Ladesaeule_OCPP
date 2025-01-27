

from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.Ports import *
from sys_basis.Manager_Coroutine import ManagerCoroutines
from sys_basis.GPIO import GPIOManager
import datetime
from tools.data_gene import DataGene
from const.Const_Parameter import *
from const.Charge_Point_Parameters import *


_info = Log.RAS.info
_error = Log.RAS.error
_debug = Log.RAS.debug
_exception = Log.RAS.exception


class Client:
    def __init__(self):
        self.init_parameters()
        self.init_threads()
        self.init_coroutines()
        self.init_signal_connections()
        self.thread_web_server.start()
        self.manager_coroutines.start()

    def init_parameters(self) -> None:
        self.GPIO_Manager = GPIOManager()

    def init_threads(self) -> None:
        self.thread_web_server = PortWebServerChargePoint()

    def init_coroutines(self) -> None:
        self.coroutine_OCPP_client = PortOCPPWebsocketClient(
            uri=f'{CP_Params.HOST}:{CP_Params.PORT}',
            charge_point_name='CP1',
            recv_timeout_s=CP_Params.RECEIVE_TIMEOUT,
            ocpp_response_timeout_s=CP_Params.RESPONSE_TIMEOUT,
            ping_interval_s=CP_Params.PING_INTERVAL,
            ping_timeout_s=CP_Params.PING_TIMEOUT,
            listen_timeout_s=CP_Params.OCPP_LISTEN_INTERVAL
        )
        self.coroutine_gui_websocket_server = PortWebSocketServer('localhost', 12346)
        self.manager_coroutines = ManagerCoroutines(self.coroutine_OCPP_client.run, self.coroutine_gui_websocket_server.run)

    def init_signal_connections(self) -> None:
        """ 信号连接 """
        # 显示信息处理
        # self.coroutine_gui_websocket_server.signal_thread_websocket_client_info.connect(self.send_info_gui_message)
        # self.coroutine_OCPP_client.signal_thread_ocpp_client_info.connect(self.send_info_web_message)
        # self.thread_web_server.signal_thread_web_server_info.connect(self.send_info_web_message)
        Log.RAS.signal_log_public_html.connect(self.send_message_to_web)

        # # 接收原始 ocpp 数据
        # self.coroutine_OCPP_client.signal_thread_ocpp_client_recv.connect(self.send_message_to_web)

        # 处理 优化器的 OCPP 的请求, 响应，响应结果
        self.coroutine_OCPP_client.signal_thread_ocpp_client_recv_request.connect(self.handle_request)
        self.coroutine_OCPP_client.signal_thread_ocpp_client_recv_response.connect(self.handle_response)
        self.coroutine_OCPP_client.signal_thread_ocpp_client_recv_response_result.connect(self.handle_response_result)

        # 处理优化器的 普通消息
        self.coroutine_OCPP_client.signal_thread_ocpp_client_normal_message.connect(self.handle_normal_message)

        # 处理网页端的消息
        self.thread_web_server.signal_thread_web_server_recv.connect(self.handle_web_message)

        # 处理电脑端的消息
        self.coroutine_gui_websocket_server.signal_thread_websocket_client_recv.connect(self.handle_computer_message)

        # 处理 GPIO 的消息
        self.GPIO_Manager.signal_request_charge_plan_calibration.connect(self.handle_gpio_requeset)
        self.GPIO_Manager.signal_GPIO_info.connect(self.handle_gpio_info)

    def handle_request(self, request_message):
        pass

    def handle_response(self, response_message):
        pass

    def handle_response_result(self, response_result_message):
        pass

    def handle_normal_message(self, normal_message):
        pass

    def handle_web_message(self, web_message):
        pass

    def handle_computer_message(self, computer_message):
        pass

    def handle_gpio_requeset(self, gpio_request):
        pass

    def handle_gpio_info(self, gpio_info):
        pass

    def send_message_to_web(self, message):
        pass

    def send_info_web_message(self, message):
        if not message:
            return
        # print(message, type(message))
        temp_dict = {
            'client_console': message
        }
        self.thread_web_server.send_message(temp_dict)
        # if message == 'home':
        #     self.send_test()
        # elif message == 'home1':
        #     self.send_test1()
        if isinstance(message, dict):
            cnrq = GenNotifyEVChargingNeedsRequest
            request_message = cnrq.generate(
                charging_needs=cnrq.get_charging_needs(
                    requested_energy_transfer=EnergyTransferModeType.ac_three_phase,
                    ac_charging_parameters=cnrq.get_ac_charging_parameters(
                        energy_amount=int(message['charge_power']),
                        ev_min_current=6,
                        ev_max_current=40,
                        ev_max_voltage=400
                    ),
                    departure_time=message['departure_time']
                ),
                evse_id=1,
                custom_data=cnrq.get_custom_data(vendor_id='12123', mod=int(message['charge_mode']))
            )
            self.coroutine_OCPP_client.send_request_message(request_message)

    def send_info_opt_message(self, message):
        temp_dict = {
            'opt_console': message
        }
        self.thread_web_server.send_message(temp_dict)

    def send_info_gui_message(self, message):
        temp_dict = {
            'gui_websocket_console': message
        }
        self.thread_web_server.send_message(temp_dict)

    def handle_gpio_data(self, data: dict):
        """
        {
            'evse_id': str,  # EVSE的ID
            'current_current': float,  # 当前电流
            'current_Voltage': float,  # 当前电压
            'current_power': float,  # 当前功率
            'current_status': ['free', 'charging'],  # 当前状态
            'start_charge_time': [None, '实际时间戳, 使用time.time()获取'],  # 开始充电时间戳
            'charged_energy': [None, float],  # 已充电能量, 单位是瓦时 Wh
            'charged_time_h': [None, float],  # 已充电时间, 单位是小时 h, 与charge_time_s等价, 只是单位不同
            'charged_time_s': [None, float],  # 已充电时间, 单位是秒 s, 与charge_time_h等价, 只是单位不同
            # ... 其他引脚状态等信息
        }

        """
        curent = data.get('current_current', 0)
        voltage = data.get('current_voltage', 0)
        power = data.get('current_power', 0)
        charge_status = data.get('current_status', 0)
        charge_start_time = data.get('start_charge_time', 0)
        charged_energy = data.get('charged_energy', 0)
        charged_time_h = data.get('charged_time_h', 0)
        # 发送消息
        message = {
            'current': curent,
            'voltage': voltage,
            'power': power,
            'charge_status': charge_status,
            'charge_start_time': charge_start_time,
            'charged_energy': charged_energy,
            'charged_time_h': charged_time_h,
        }
        self.send_info_web_message(message)
        self.send_info_gui_message(message)
        # 处理充电动作
        if curent <= 0 and charge_status == 'charging':
            # 停止充电处理
            pass
        elif charge_status == 'free':
            # 准备充电处理
            pass
        else:  # curent > 0 & charge_status == 'charging'
            # 充电处理
            pass

    def send_test(self):
        if self.coroutine_OCPP_client.websocket.isConnected:
            try:
                _info('发送测试数据')
                # self.coroutine_OCPP_client.send_normal_message('这是一个普通的测试信息******')
                self.coroutine_OCPP_client.send_request_message(GenNotifyEVChargingNeedsRequest.load_dict({
                    "evseId": 1,
                    "chargingNeeds": {
                        "requestedEnergyTransfer": EnergyTransferModeType.ac_three_phase,
                        "acChargingParameters": {
                            "energyAmount": 70000,
                            "evMaxCurrent": 40,
                            "evMinCurrent": 6,
                            "evMaxVoltage": 400,
                        },
                        "departureTime": DataGene.time2str(datetime.datetime.now() + datetime.timedelta(hours=10))
                    },
                    "customData": GenNotifyEVChargingNeedsRequest.get_custom_data(vendor_id='12123', mod=0)})
                )
                _info(len(self.coroutine_OCPP_client.list_request_message), self.coroutine_OCPP_client.list_request_message)
            except:
                _exception()
                pass
        # self._num += 1
        # if self._num <= 10:
        #     self.__timer = threading.Timer(10, self.send_test)
        #     self.__timer.start()

    def send_test1(self):
        self.coroutine_OCPP_client.send_request_message(
            GenAuthorizeRequest.generate(
                id_token=GenAuthorizeRequest.get_id_token('想不到是中文吧, 哈哈哈哈', IdTokenType.central),
            )
        )

    def rrr(self, message):
        _info(f'收到消息: {message}')
        if message['action'] == Action.SetChargingProfile:
            self.coroutine_OCPP_client.send_response_message(
                Action.SetChargingProfile,
                GenSetChargingProfileResponse.generate(
                    status=ChargingProfileStatus.accepted
                ),
                send_time=message['send_time'],
                message_id=message['message_id']
            )

    def handle_normal_message(self, message: dict) -> None:

        if 'opt_img' in message:
            _info(f'收到消息: {message}')
            self.send_info_web_message(message['opt_img'])
