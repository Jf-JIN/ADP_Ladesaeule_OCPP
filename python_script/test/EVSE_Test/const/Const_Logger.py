
from DToolslib import *
import os
APP_WP = os.path.dirname(os.path.dirname(__file__))


class Log(StaticEnum):
    logging = Logger('Logging', root_dir=APP_WP)
    CRITICAL = Logger('Critical', root_dir=APP_WP)
    SOCKET = Logger('Socket_Core', root_dir=APP_WP)
    MODBUS = Logger('Modbus_Handler', root_dir=APP_WP)
    UI = Logger('UI', root_dir=APP_WP)
    SERVER = Logger('Server', root_dir=APP_WP)
    GPIO = Logger('GPIO', root_dir=APP_WP)
    GROUP = LoggerGroup(root_dir=APP_WP)


Log.logging.set_listen_logging()
for log in Log:
    log: Logger
    if not isinstance(log, LoggerGroup):
        log.set_file_count_limit(10)
        log.set_level(LogLevel.INFO)
