
import os
from const.Analog_Define import AnalogDefine
from tools.Logger import Logger, LoggerGroup

os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()


class Log(AnalogDefine):
    __EXCLUDE_FUNCS = ['_send_signal_info', '__send_signal_recv', '__send_signal_info', '__send_signal']
    RAS = Logger(log_name='client_rasberryPi', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='client_rasberryPi', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    CSMS = Logger(log_name='csms', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='csms', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    WS = Logger(log_name='websocket', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='websocket', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    CP = Logger(log_name='charge_point', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='charge_point',
                count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    OCPP = Logger(log_name='ocpp_port', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='ocpp_port', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    WEB = Logger(log_name='web', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='web_server', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    GPIO = Logger(log_name='gpio', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='gpio', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    OPT = Logger(log_name='optimize', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='optimize', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    GUI = Logger(log_name='gui_port', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='gui_port', count_limit=10, exclude_funcs=__EXCLUDE_FUNCS)
    GROUP = LoggerGroup(log_folder_path=APP_WORKSPACE_PATH, count_limit=10, size_limit=100)
