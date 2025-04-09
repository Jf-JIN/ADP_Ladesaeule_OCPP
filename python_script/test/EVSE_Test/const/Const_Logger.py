from DToolslib import *


class Log(StaticEnum):
    SOCKET = Logger('Socket_Core', log_level=LogLevel.DEBUG)
    MODBUS = Logger('Modbus_Handler', log_level=LogLevel.DEBUG)
