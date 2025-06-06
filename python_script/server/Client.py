

import functools
import subprocess
import time
from const.GPIO_Parameter import *
from tools.Logger import Logger
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.Ports import *
from sys_basis.CSV_Loader import *
from sys_basis.Manager_Coroutine import ManagerCoroutines
from sys_basis.GPIO._Charge_Unit import ChargeUnit
from sys_basis.GPIO import GPIOManager
from sys_basis.GPIO._Manager_LED import *
import datetime
from tools.data_gene import DataGene
from const.Const_Parameter import *
from const.Charge_Point_Parameters import *
import json
from sys_basis.GPIO._Shelly_Data_CSV_Writer import ShellyDataCSVWriter

_log: Logger = Log.RAS


class Client:
    def __init__(self):
        self.init_parameters()
        self.init_threads()
        self.init_coroutines()
        self.init_signal_connections()
        self.thread_web_server.start()
        time.sleep(0.5)
        self.GPIO_Manager.listening_start()
        self.manager_coroutines.start()

    def init_parameters(self) -> None:
        self.GPIO_Manager = GPIOManager()
        self.__cp_info_dict: dict = {}
        self.__csv_loader = CSVLoader(self)  # singleton
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
        if hasattr(self, 'GPIO_Manager'):
            self.GPIO_Manager.stop()
            # self.GPIO_Manager = None
        if hasattr(self, 'thread_web_server'):
            self.thread_web_server.stop()
            # self.thread_web_server = None
        if hasattr(self, 'manager_coroutines'):
            self.manager_coroutines.stop()
            # self.manager_coroutines = None
        # os._exit(0)

    def __del__(self):
        self.stop()

    def init_signal_connections(self) -> None:
        """ 信号连接 """
        # 显示信息处理
        # self.coroutine_gui_websocket_server.signal_thread_websocket_client_info.connect(self.send_info_gui_message)
        # self.coroutine_OCPP_client.signal_thread_ocpp_client_info.connect(self.send_info_web_message)
        # self.thread_web_server.signal_thread_web_server_info.connect(self.send_info_web_message)
        Log.RAS.signal_all_color.connect(self.send_web_console_message)
        Log.CP.signal_all_color.connect(self.send_web_console_message)
        Log.GPIO.signal_all_color.connect(self.send_web_console_message)
        Log.GROUP.signal_error_message.connect(self.send_web_error_message)
        Log.GROUP.signal_critical_message.connect(self.send_web_error_message)

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
        self.GPIO_Manager.signal_GPIO_info.connect(self.send_web_alert_message)
        self.GPIO_Manager.signal_GPIO_info.connect(self.handle_gpio_info)
        self.GPIO_Manager.data_collector.signal_DC_data_display.connect(self.send_web_txt_message)
        self.GPIO_Manager.data_collector.signal_DC_watching_data_display.connect(self.send_web_watching_data_message)
        self.GPIO_Manager.data_collector.signal_DC_figure_display.connect(self.send_web_data_manager_fig_message)

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
                if not self.GPIO_Manager.get_charge_unit(evse_id).isCharging:
                    self.send_web_alert_message('已成功接收到优化后的充电计划\nThe charging plan has been successfully received', 'success')
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
            'opt_result': ('opt_fig', self.send_web_optimization_result_message),
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
        _log.debug(f'接收消息\nReceiving message\n{web_message}')
        handle_dict = {
            # 接收的消息标签: (给Web发送消息的标签, 处理函数)
            'charge_request': self.web_handle_charge_request,
            'charge_now': self.web_handle_charge_now,
            'stop': self.web_handle_charge_stop,
            'reset_raspberry_pi_no_error': self.web_handle_reset_no_error,
            'manual_input': self.web_handle_manual_input,
            'manual_input_csv': self.web_handle_manual_input_csv,
            'logout': self.web_handle_logout,
            'download_csv': self.web_handle_download_csv,
            'time_synchronize': self.web_handle_time_synchronize,
        }
        if not isinstance(web_message, dict):
            if isinstance(web_message, str):
                try:
                    web_message = json.loads(web_message)
                except:
                    _log.warning(f"消息格式错误 Message format error\n{web_message}")
                    return
            else:
                _log.warning(f"消息格式错误 Message format error\n{web_message}")
                return
        for key, value in handle_dict.items():
            if key in web_message:
                value(web_message[key])

    def web_handle_charge_request(self, request_message):
        _log.debug(f"收到充电请求 Receive charging request:\n{request_message}")
        evse_id = int(request_message['evse_id'])
        mode = int(request_message['charge_mode'])
        if mode >= 0:
            energy_amount = int(request_message['charge_power'])
            depart_time = request_message['depart_time']
        else:
            energy_amount = 0
            depart_time = ''
        if not depart_time.endswith('Z'):
            if depart_time.count(':') == 1:
                depart_time += ':00Z'
            elif depart_time.count(':') == 2:
                depart_time += 'Z'
        if evse_id not in self.GPIO_Manager.data_collector.available_charge_units_id_set or self.GPIO_Manager.get_charge_unit(evse_id).isCharging:
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
        if mode not in [0, 1, 2]:
            self.send_web_alert_message('当前模式无需提交数据\nCurrent mode does not need to submit data', message_type='info')
            return

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
            _log.info('已成功向优化器发送请求\nRequest sent to optimizer successfully')
            self.send_web_alert_message('已成功向优化器发送请求\nRequest sent to optimizer successfully', message_type='info')
        except:
            _log.exception()
            self.send_web_error_message('充电请求失败\nCharging request failed')

    def web_handle_charge_now(self, charge_now_dict: dict):
        _log.debug(f'收到立即充电请求:\nReceive the immediately charging request\n{charge_now_dict}')
        evse_id = int(charge_now_dict['evse_id'])
        charge_mode = int(charge_now_dict['charge_mode'])
        if charge_mode == -1:
            enableDirectCharge = True
        else:
            enableDirectCharge = False
        res = self.GPIO_Manager.get_charge_unit(evse_id).start_charging(enableDirectCharge)
        # if not res:
        #     _log.error('立即充电失败\nimmediately charging failed')

    def web_handle_charge_stop(self, charge_stop_dict: dict):
        _log.info(f'收到停止充电请求:\nReceive the stop charging request\n{charge_stop_dict}')
        evse_id = int(charge_stop_dict['evse_id'])
        self.GPIO_Manager.get_charge_unit(evse_id).stop_charging(sender='web')

    def web_handle_reset_no_error(self, charge_stop_dict: dict):
        _log.info(f'收到重置请求:\nReceive the reset request\n{charge_stop_dict}')
        evse_id = int(charge_stop_dict['evse_id'])
        self.GPIO_Manager.get_charge_unit(evse_id).clear_error()

    def web_handle_manual_input(self, manual_input_dict: dict):
        _log.info(f'收到手动输入请求:\nReceive the manual input request\n{manual_input_dict}')
        if not manual_input_dict:
            _log.warning('手动输入请求为空\nManual input request is empty')
            self.send_web_alert_message('手动输入请求为空\nManual input request is empty', 'warning')
        data: dict | None = CSVLoader.getData()
        if not data:
            self.send_web_alert_message('未上传文件\nhas not uploaded the file', 'warning')
            _log.warning(f'未上传文件\nhas not uploaded the file')
            return
        evse_id = int(data.get('evseId', -1))
        if evse_id < 0 or evse_id not in self.GPIO_Manager.charge_units_dict:
            id_list = list(self.GPIO_Manager.charge_units_dict.keys())
            self.send_web_error_message(f'EVSE ID 错误, 可用ID {id_list}\nEVSE ID error, available ID {id_list}')
            return
        if evse_id not in self.__cp_info_dict:
            self.__cp_info_dict[evse_id] = {
                'target_energy': float(manual_input_dict.get('target_energy', 0)),
                'depart_time': manual_input_dict.get('depart_time', datetime.now().replace(microsecond=0).isoformat() + 'Z'),
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

    def web_handle_manual_input_csv(self, csv_file) -> None:
        csv_file = csv_file['data']
        if not csv_file:
            return
        if csv_file == 'clear':
            if not CSVLoader.getData():
                return
            CSVLoader.clear()
            self.send_web_alert_message('已清空充电计划CSV文件\nThe charging plan CSV file has been cleared', 'success')
            return
        res = CSVLoader.loadCSV(csv_file)
        if isinstance(res, str):
            self.send_web_error_message('CSV文件格式错误\nCSV file format error\n\n'+res)
            return

    def web_handle_logout(self, enable: bool) -> None:
        _log.info(f'关闭程序 Close the Programm\t{enable}')
        if enable:
            self.stop()
            sys.exit(0)
        else:
            # os.execv(sys.executable, ['python'] + sys.argv)
            self.send_web_alert_message('Not suported yet.')

    def web_handle_download_csv(self, download_num: dict) -> None:
        _log.info('下载shelly_CSV文件 Download the shelly CSV file')
        if 'num' in download_num:
            num = download_num['num']
        else:
            num = 1
        if 'id' in download_num:
            id = download_num['id']
        else:
            id = 1
        self.send_web_alert_message('打包CSV文件中...\nPacked in CSV file...', 'info')
        self.GPIO_Manager.get_charge_unit(id).shelly_writer.signal_exported_file_path.connect(self.web_send_download_csv)
        self.GPIO_Manager.get_charge_unit(id).shelly_writer.request_exported_csv_files_path(num)

    def web_handle_time_synchronize(self, sync_time_dict: dict) -> None:
        if 'target_time' not in sync_time_dict:
            return
        target_time = sync_time_dict['target_time']
        try:
            result = subprocess.run(['date', '-s', target_time], capture_output=True, text=True)

            if result.returncode == 0:
                res_str = result.stdout.strip()
                _log.info(f"Time synchronized: {res_str}")
            else:
                _log.error("Error: %s", result.stderr.strip())
                self.send_web_alert_message('同步时间失败\nFailed to synchronize time', 'error')
        except:
            self.send_web_alert_message('同步时间失败\nFailed to synchronize time', 'error')
            return

    def web_send_download_csv(self, path: str) -> None:
        _log.info('打包完成，准备发送文件 Packed, ready to send file')
        if not os.path.exists(path):
            self.thread_web_server.send_csv_data({'error': 'File not found'})
            self.send_web_error_message('文件未找到\nFile not found')
            return
        filename = os.path.basename(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.thread_web_server.send_csv_data({
            'filename': filename,
            'content': content
        })

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

    def handle_gpio_info(self, gpio_info, *args, **kwargs) -> None:
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

    def send_web_optimization_result_message(self, message: dict) -> None:
        message = message['opt_fig']
        if 'opt_img' in message:
            self.send_message_to_web('figure', {'opt_fig': message['opt_img']})
        # _log.info(message)
        _log.info(message['result'])
        if message['result'] == 0:  # 失败
            self.send_web_alert_message('充电计划表优化失败\nCharging plan optimization failed', 'error')
        elif message['result'] == 1:  # 成功
            self.send_web_alert_message('已成功收到充电计划表\nCharging plan received successfully', 'success')

    def send_web_data_manager_fig_message(self, message: dict) -> None:
        self.send_message_to_web('figure', message)

    def send_web_txt_message(self, message) -> None:
        self.send_message_to_web('txt', message)

    def send_web_watching_data_message(self, message) -> None:
        self.send_message_to_web('watching_data', message)

    def send_web_alert_message(self, message: str, message_type='info') -> None:
        _log.info('message from server to web:\n'+message)
        self.send_message_to_web('alert_message', {"type": message_type, "message": message.replace('\n', '<br>')})

    def send_web_error_message(self, message) -> None:
        self.send_web_alert_message(message, 'error')
        # _log.error(message)

    def __send_response_message(self, response_message, request_message) -> None:
        self.coroutine_OCPP_client.send_response_message(
            request_message['action'],
            response_message,
            send_time=request_message['send_time'],
            message_id=request_message['message_id']
        )
