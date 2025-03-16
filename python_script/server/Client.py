

import time
from const.GPIO_Parameter import GPIOParams
from tools.Logger import Logger
from sys_basis.GPIO._Charge_Unit import ChargeUnit
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.Ports import *
from sys_basis.Manager_Coroutine import ManagerCoroutines
from sys_basis.GPIO import GPIOManager
import datetime
from tools.data_gene import DataGene
from const.Const_Parameter import *
from const.Charge_Point_Parameters import *
import json

_log: Logger = Log.RAS


class Client:
    def __init__(self):
        self.init_parameters()
        self.init_threads()
        self.init_coroutines()
        self.init_signal_connections()
        self.thread_web_server.start()
        time.sleep(1)
        self.GPIO_Manager.listening_start()
        self.manager_coroutines.start()

    def init_parameters(self) -> None:
        self.GPIO_Manager = GPIOManager()
        self.__cp_info_dict: dict = {}
        """ 该字典主要记录各个evse的充电需求信息, 如离开时间, 充电总量,其他信息 """

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
        self.manager_coroutines = ManagerCoroutines(self.coroutine_OCPP_client, self.coroutine_gui_websocket_server)

    def stop(self):
        self.GPIO_Manager.stop()
        self.thread_web_server.stop()
        self.manager_coroutines.stop()

    def __del__(self):
        self.stop()

    def init_signal_connections(self) -> None:
        """ 信号连接 """
        # 显示信息处理
        # self.coroutine_gui_websocket_server.signal_thread_websocket_client_info.connect(self.send_info_gui_message)
        # self.coroutine_OCPP_client.signal_thread_ocpp_client_info.connect(self.send_info_web_message)
        # self.thread_web_server.signal_thread_web_server_info.connect(self.send_info_web_message)
        Log.RAS.signal_log_public_html.connect(self.send_web_console_message)

        # # 接收原始 ocpp 数据
        # self.coroutine_OCPP_client.signal_thread_ocpp_client_recv.connect(self.send_message_to_web)

        # 处理 优化器的 OCPP 的请求, 响应, 响应结果
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
        self.GPIO_Manager.data_collector.signal_DC_data_display.connect(self.send_web_txt_message)
        self.GPIO_Manager.data_collector.signal_DC_figure_display.connect(self.send_web_fig_message)

    def handle_request(self, request_message) -> None:
        """
        处理 OCPP 请求消息

        request_message 内容格式
        - `action`(str): 消息类型
        - `data`(dict): OCPP消息的字典形式
        - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        """
        # TODO 可以增加判断逻辑
        # TODO 该函数可以优化, 并拆分小模组/模块
        response_message_dict: dict = {
            Action.set_charging_profile: GenSetChargingProfileResponse.generate(
                status=ChargingProfileStatus.accepted
            ),
        }
        response_message: str = response_message_dict.get(request_message['action'], None)
        if response_message:
            self.__send_response_message(response_message, request_message)
            if request_message['action'] == Action.set_charging_profile:
                evse_id = request_message['data']['evseId']
                res: bool = self.GPIO_Manager.set_charge_plan(
                    data=request_message['data'],
                    target_energy=self.__cp_info_dict[evse_id]['target_energy'],
                    depart_time=self.__cp_info_dict[evse_id]['depart_time'],
                    custom_data=self.__cp_info_dict[evse_id]['custom_data']
                )
                if not res:
                    self.send_web_error_message('设置充电计划失败\nSet up the charging plan failed')

    def handle_response(self, response_message: dict) -> None:
        """
        处理 OCPP 响应消息

        response_message 内容格式
        - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
        - `ori_data`: 原始数据, 发送的Request数据
        - `data`(dict): 解包后的数据
        - `send_time`(float): 请求发送时间
        - `result`(int): 响应结果,
            - 枚举类 `CP_Params.RESPONSE`
            - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        """
        if response_message['result'] == CP_Params.RESPONSE.TIMEOUT:
            self.coroutine_OCPP_client.send_request_message(response_message['ori_data'])

    def handle_response_result(self, response_result_message):
        """
        处理 OCPP 响应结果消息, 此方法可以在 顺序敏感 的情况下使用

        response_result_message 内容格式
        - `action`(str): 消息类型
        - `data`(dict): OCPP消息的字典形式
        - `send_time`(float): 接收的信号中的时间戳
        - `result`(int): 发送结果
            - 枚举类 `CP_Params.RESPONSE_RESULT`
            - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        """
        pass

    def handle_normal_message(self, normal_message):
        """
        处理 OCPP端口 普通消息
        """
        handle_dict = {
            # 接收的消息标签: (给Web发送消息的标签, 处理函数)
            'opt_img': ('opt_fig', self.send_web_fig_message),
        }
        for key, value in handle_dict.items():
            if key in normal_message:
                func = value[1]
                label = value[0]
                temp_dict = {label: normal_message[key]}
                func(temp_dict)

    def handle_web_message(self, web_message):
        """
        处理 Web端 消息
        """
        def handle_web_charge_request(request_message):
            _log.info(f"收到充电请求 Receive charging request:\n{request_message}")
            evse_id = int(request_message['evse_id'])
            energy_amount = int(request_message['charge_power'])
            depart_time = request_message['depart_time']
            mode = int(request_message['charge_mode'])
            if evse_id not in self.GPIO_Manager.data_collector.available_charge_units_id_set:
                self.send_web_error_message('EVSE_ID不可用\nevse_id is not available')
                return
            charge_unit: ChargeUnit = self.GPIO_Manager.get_charge_unit(evse_id)
            if not charge_unit.isAvailabel:
                self.send_web_error_message('充电单元不可用\ncharge_unit is not available')
                return
            current_limit_list = self.GPIO_Manager.get_current_limit(evse_id)
            voltage_max = self.GPIO_Manager.get_voltage_max(evse_id)
            _log.info(f""" \
已获取 Obtain
evse_id:{evse_id},
energy_amount: {energy_amount},
depart_time:{depart_time},
mode:{mode},
current_limit_list:{current_limit_list},
voltage_max:{voltage_max}
""")
            if current_limit_list is None or len(current_limit_list) == 0:
                self.send_web_error_message('获取电流限制错误\nget current_limit error')
                return
            self.__cp_info_dict[evse_id] = {
                'target_energy': energy_amount,
                'depart_time': depart_time,
                'custom_data': {"vendor_id": GPIOParams.VENDOR_ID, "mode": mode},
            }
            try:
                g = GenNotifyEVChargingNeedsRequest
                self.coroutine_OCPP_client.send_request_message(
                    g.generate(
                        evse_id=evse_id,
                        charging_needs=g.get_charging_needs(
                            requested_energy_transfer=EnergyTransferModeType.ac_three_phase,
                            ac_charging_parameters=g.get_ac_charging_parameters(
                                energy_amount=energy_amount,
                                ev_max_voltage=voltage_max,
                                ev_max_current=current_limit_list[1],
                                ev_min_current=current_limit_list[0],
                            ),
                            departure_time=depart_time,
                        ),
                        custom_data=g.get_custom_data(vendor_id=GPIOParams.VENDOR_ID, mode=mode)
                    )
                )
            except:
                _log.exception()
                self.send_web_error_message('充电请求失败\nCharging request failed')

        def handle_charge_now(charge_now_dict: dict):
            _log.info(f'收到立即充电请求:\nReceive the immediately charging request\n{charge_now_dict}')
            evse_id = int(charge_now_dict['evse_id'])
            charge_mode = int(charge_now_dict['charge_mode'])
            if charge_mode == -1:
                enableDirectCharge = True
            else:
                enableDirectCharge = False
            res = self.GPIO_Manager.get_charge_unit(evse_id).start_charging(enableDirectCharge)
            if not res:
                _log.error('立即充电失败\nimmediately charging failed')

        def handle_charge_stop(charge_stop_dict: dict):
            _log.info(f'收到停止充电请求:\nReceive the stop charging request\n{charge_stop_dict}')
            evse_id = int(charge_stop_dict['evse_id'])
            self.GPIO_Manager.get_charge_unit(evse_id).stop_charging()

        def handle_reset_no_error(charge_stop_dict: dict):
            _log.info(f'收到重置请求:\nReceive the reset request\n{charge_stop_dict}')
            evse_id = int(charge_stop_dict['evse_id'])
            self.GPIO_Manager.get_charge_unit(evse_id).clear_error()

        def handle_manual_input(manual_input_dict: dict):
            _log.info(f'收到手动输入请求:\nReceive the manual input request\n{manual_input_dict}')
            if not manual_input_dict:
                _log.error('手动输入请求为空\nManual input request is empty')

            if isinstance(manual_input_dict['data'], str):
                try:
                    data: dict = json.loads(manual_input_dict['data'])
                except:
                    data = manual_input_dict['data']
                    _log.error(f'手动输入请求格式错误\nManual input request format error\n{data}')
                    return
            else:
                data: dict = manual_input_dict['data']
            evse_id = int(data.get('evseId', -1))
            _log.critical(evse_id, data)
            if not data or evse_id < 0:
                _log.error(f'data 错误\nError in data\n{data}')
                return
            if evse_id not in self.__cp_info_dict:
                self.__cp_info_dict[evse_id] = {
                    'target_energy': float(manual_input_dict.get('target_energy', 0)),
                    'depart_time': manual_input_dict.get('target_energy', datetime.datetime.now().replace(microsecond=0).isoformat() + 'Z'),
                    'custom_data': {"vendor_id": GPIOParams.VENDOR_ID, "mode": 0},
                }
            res: bool = self.GPIO_Manager.set_charge_plan(
                data=data,
                target_energy=self.__cp_info_dict[evse_id]['target_energy'],
                depart_time=self.__cp_info_dict[evse_id]['depart_time'],
                custom_data=self.__cp_info_dict[evse_id]['custom_data'],
                isManual=True
            )
            if not res:
                self.send_web_error_message('设置充电计划失败\nSet up the charging plan failed')
                return
            self.GPIO_Manager.get_charge_unit(evse_id).start_charging()

        _log.debug(f'接收消息\nReceiving message\n{web_message}')
        handle_dict = {
            # 接收的消息标签: (给Web发送消息的标签, 处理函数)
            'charge_request': handle_web_charge_request,
            'charge_now': handle_charge_now,
            'stop': handle_charge_stop,
            'reset_raspberry_pi_no_error': handle_reset_no_error,
            'manual_input': handle_manual_input
        }
        for key, value in handle_dict.items():
            if key in web_message:
                value(web_message[key])

    def handle_computer_message(self, computer_message) -> None:
        """
        处理 电脑端 消息
        """
        _log.info(f'收到电脑端信息\nReceive the computer information\n{computer_message}')

    def handle_gpio_requeset(self, gpio_request) -> None:
        """
        处理 GPIO 请求消息, 请求频率由GPIOManager控制

        控制量可在 `GPIOParams.CALIBRATION_PERIOD` 中修改

        请求(dict)的键名:
        - `evseId`: (int),
        - `evMinCurrent`: (int),
        - `evMaxCurrent`: (int),
        - `evMaxVoltage`: (int),
        - `energyAmount`: (int),
        - `departureTime`: (str),
        - `custom_data`: (dict)
        """
        try:
            g = GenNotifyEVChargingNeedsRequest
            self.coroutine_OCPP_client.send_request_message(
                g.generate(
                    evse_id=gpio_request['evseId'],
                    charging_needs=g.get_charging_needs(
                        requested_energy_transfer=EnergyTransferModeType.ac_three_phase,
                        ac_charging_parameters=g.get_ac_charging_parameters(
                            energy_amount=gpio_request['energyAmount'],
                            ev_max_voltage=gpio_request['evMaxVoltage'],
                            ev_max_current=gpio_request['evMaxCurrent'],
                            ev_min_current=gpio_request['evMinCurrent'],
                        ),
                        departure_time=gpio_request['departureTime'],
                    ),
                    custom_data=g.get_custom_data(vendor_id=gpio_request['custom_data']['vendor_id'], mode=gpio_request['custom_data']['mode'])
                )
            )
        except:
            _log.exception()

    def handle_gpio_info(self, gpio_info):
        pass

    def send_message_to_web(self, category, message) -> None:
        temp_dict: dict = {
            category: message
        }
        self.thread_web_server.send_message(temp_dict)

    def send_web_console_message(self, message) -> None:
        self.send_message_to_web('console', message)

    def send_web_opt_message(self, message) -> None:
        self.send_message_to_web('opt_console', message)

    def send_web_gpio_message(self, message) -> None:
        self.send_message_to_web('gpio_console', message)

    def send_web_fig_message(self, message) -> None:
        self.send_message_to_web('figure', message)

    def send_web_txt_message(self, message) -> None:
        self.send_message_to_web('txt', message)

    def send_web_error_message(self, message) -> None:
        self.send_message_to_web('error', message)
        _log.error(message)

    def __send_response_message(self, response_message, request_message) -> None:
        self.coroutine_OCPP_client.send_response_message(
            request_message['action'],
            response_message,
            send_time=request_message['send_time'],
            message_id=request_message['message_id']
        )
