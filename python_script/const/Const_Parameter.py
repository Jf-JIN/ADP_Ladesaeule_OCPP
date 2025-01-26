
import os
from const.Analog_Define import AnalogDefine
from tools.Logger import LogLevel, Logger, LoggerGroup

os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()


class Log(AnalogDefine):
    __EXCLUDE_FUNCS = ['_send_signal_info', '__send_signal_recv', '__send_signal_info', '__send_signal', '_log', 'log', 'who_called_me']
    __EXCLUDE__CLASSES = []
    __EXCLUDE_MODULES = ['server', 'serving', ]
    __COUNT_LIMIT = 30
    RAS = Logger(
        log_name='client_rasberryPi', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='client_rasberryPi',
        count_limit=10, exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    CSMS = Logger(
        log_name='csms', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='csms', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    WS = Logger(
        log_name='websocket', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='websocket', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    CP = Logger(
        log_name='charge_point', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='charge_point',
        count_limit=10, exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    OCPP = Logger(
        log_name='ocpp_port', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='ocpp_port', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    WEB = Logger(
        log_name='web', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='web_server', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    GPIO = Logger(
        log_name='gpio', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='gpio', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    MODBUS = Logger(
        log_name='modbus', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='modbus', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    SHELLY = Logger(
        log_name='shelly', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='shelly', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    EVSE = Logger(
        log_name='evse', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='evse', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    OPT = Logger(
        log_name='optimize', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='optimize', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    GUI = Logger(
        log_name='gui_port', log_folder_path=APP_WORKSPACE_PATH, log_sub_folder_name='gui_port', count_limit=__COUNT_LIMIT,
        exclude_funcs=__EXCLUDE_FUNCS, exclude_classes=__EXCLUDE__CLASSES, exclude_modules=__EXCLUDE_MODULES
    )
    GROUP = LoggerGroup(log_folder_path=APP_WORKSPACE_PATH, count_limit=__COUNT_LIMIT, size_limit=100)
