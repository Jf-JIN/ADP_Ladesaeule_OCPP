from DToolslib import *


class ModbusParams(StaticEnum):
    PORT = '/dev/ttyS0'  # 串口号
    BAUDRATE = 9600  # 波特率
    PARITY = 'N'  # 无校验位
    STOPBITS = 1  # 停止位
    BYTESIZE = 8  # 数据位
    TIMEOUT = 3  # 超时时间
    RETRIES = 10  # 重试次数
