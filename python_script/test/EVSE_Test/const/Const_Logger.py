
from DToolslib import *
import os
APP_WP = os.path.dirname(os.path.dirname(__file__))


class Log(StaticEnum):
    logging = Logger('Logging', log_folder_path=APP_WP)
    CRITICAL = Logger('Critical', log_folder_path=APP_WP)
    SOCKET = Logger('Socket_Core', log_folder_path=APP_WP)
    MODBUS = Logger('Modbus_Handler', log_folder_path=APP_WP)
    UI = Logger('UI', log_folder_path=APP_WP)
    SERVER = Logger('Server', log_folder_path=APP_WP)
    GPIO = Logger('GPIO', log_folder_path=APP_WP)
    GROUP = LoggerGroup(log_folder_path=APP_WP, limit_files_count=10)


Log.logging.set_listen_logging()
for log in Log:
    log: Logger
    if not isinstance(log, LoggerGroup):
        log.set_file_count_limit(10)
        log.set_level(LogLevel.INFO)
