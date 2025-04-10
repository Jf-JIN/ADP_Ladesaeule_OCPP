from DToolslib import *
import os
APP_WP = os.path.dirname(os.path.dirname(__file__))


class Log(StaticEnum):
    SOCKET = Logger('Socket_Core', log_folder_path=APP_WP, log_level=LogLevel.DEBUG)
    MODBUS = Logger('Modbus_Handler', log_folder_path=APP_WP, log_level=LogLevel.DEBUG)
