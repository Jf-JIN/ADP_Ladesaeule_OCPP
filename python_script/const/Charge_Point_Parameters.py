
from const.Analog_Define import AnalogDefine


class _Response(AnalogDefine):
    SUCCESS = 0
    TIMEOUT = 1
    ERROR = 2


class _Response_Result(AnalogDefine):
    SUCCESS = 0
    TIMEOUT = 1
    ERROR = 2


class CP_Params(AnalogDefine):
    RESPONSE = _Response()
    RESPONSE_RESULT = _Response_Result()
    NETWORK_BUFFER_TIME = 1  # 网络延迟时间
    RESPONSE_DELAY_TIME = 1  # 响应延迟时间, 用于推迟到响应超时而使接收方报告超时
    PING_TIMEOUT = 10  # 心跳包超时时间
    PING_INTERVAL = 10  # 心跳包间隔时间
    RECEIVE_TIMEOUT = 10  # 接收超时时间, 作用于Websocket端口
    RESPONSE_TIMEOUT = 10  # 响应超时时间, 作用于充电桩
    HOST = 'ws://130.83.148.29'  # 优化算法器OCPP服务器地址
    PORT = 80
    # url = 'ws://192.168.43.65:1234'
    # url = 'ws://172.12.26.71:1234'
    # url = 'ws://130.83.148.29:80'
