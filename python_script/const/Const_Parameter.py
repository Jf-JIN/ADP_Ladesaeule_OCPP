
import os
from const.Analog_Define import AnalogDefine
# from tools.Logger import LogLevel, Logger, LoggerGroup
from DToolslib.Logger import *
from DToolslib import *


os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()
LOCK_FILE_PATH = os.path.join(APP_WORKSPACE_PATH, 'main_Client.lock')


class FontSize(AnalogDefine):
    """
    tools/data_gene.py 中使用, 用于决定画图字体大小
    """
    TITLE = 16
    LABEL = 14
    TEXT = 12
    TICKS = 10


class Color(AnalogDefine):
    """
tools/data_gene.py 中使用, 用于决定画图颜色
    """
    RED = '#FF6347'
    GREEN = '#2E8B57'
    BLUE = '#1E90FF'
    BLUE_BAR = '#98D8EF'


class Style(AnalogDefine):
    """
    tools/data_gene.py 中使用, 用于决定画图样式
    """
    BAR = 0
    PLOT = 1


class Log(StaticEnum):
    CRITICAL = Logger(log_name='CRITICAL', root_dir=APP_WORKSPACE_PATH)
    RAS = Logger(log_name='client_rasberryPi', root_dir=APP_WORKSPACE_PATH)
    CSMS = Logger(log_name='csms', root_dir=APP_WORKSPACE_PATH)
    WS = Logger(log_name='websocket', root_dir=APP_WORKSPACE_PATH)
    CP = Logger(log_name='charge_point', root_dir=APP_WORKSPACE_PATH)
    OCPP = Logger(log_name='ocpp_port', root_dir=APP_WORKSPACE_PATH)
    WEB = Logger(log_name='web', root_dir=APP_WORKSPACE_PATH)
    GPIO = Logger(log_name='gpio', root_dir=APP_WORKSPACE_PATH)
    MODBUS = Logger(log_name='modbus', root_dir=APP_WORKSPACE_PATH)
    SHELLY = Logger(log_name='shelly', root_dir=APP_WORKSPACE_PATH)
    EVSE = Logger(log_name='evse', root_dir=APP_WORKSPACE_PATH)
    OPT = Logger(log_name='optimize', root_dir=APP_WORKSPACE_PATH)
    GUI = Logger(log_name='gui_port', root_dir=APP_WORKSPACE_PATH)
    CSVLoader = Logger(log_name='CSV_loader', root_dir=APP_WORKSPACE_PATH)
    CSVWriter = Logger(log_name='CSV_writer', root_dir=APP_WORKSPACE_PATH)
    GROUP = LoggerGroup(root_dir=APP_WORKSPACE_PATH)


for log in Log:
    if isinstance(log, LoggerGroup):
        log.set_file_count_limit(30)
        log.set_file_size_limit_kB(100*1000)
        continue
    log: Logger
    log.set_exclude_funcs(['_send_signal_info', '__send_signal_recv', '__send_signal_info', '__send_signal', '_log', 'log', 'who_called_me', 'send_web_error_message', '_send'])
    log.set_exclude_classes(['XSignal', 'EventSignal'])
    log.set_exclude_modules(['server', 'serving', 'WebSocket_Client'])
    log.set_level(LogLevel.INFO)
    log.set_file_count_limit(30)
    log.set_file_size_limit_kB(20*1000)
    log.set_highlight_type(LogHighlightType.HTML)
    log.set_enable_runtime_zip(False)
