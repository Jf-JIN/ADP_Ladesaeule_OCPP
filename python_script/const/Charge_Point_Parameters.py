
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
    NETWORK_BUFFER_TIME = 10  # 网络延迟时间
    RESPONSE_DELAY_TIME = 1  # 响应延迟时间, 用于推迟到响应超时而使接收方报告超时
    PING_TIMEOUT = 10  # 心跳包超时时间
    PING_INTERVAL = 10  # 心跳包间隔时间
    RECEIVE_TIMEOUT = 30  # 接收超时时间, 作用于Websocket端口
    RESPONSE_TIMEOUT = 30  # 响应超时时间, 作用于充电桩
    OCPP_LISTEN_INTERVAL = 1  # OCPP监听间隔时间
    DO_SEND_DEFAULT_RESPONSE = False  # 是否在规定的响应时间内发送默认响应
    HOST = 'ws://130.83.148.29'  # 优化算法器OCPP服务器地址
    # HOST = 'ws://172.18.9.26'  # 优化算法器OCPP服务器地址
    PORT = 80
    # url = 'ws://192.168.43.65:1234'
    # url = 'ws://172.12.26.71:1234'
    # url = 'ws://130.83.148.29:80'
